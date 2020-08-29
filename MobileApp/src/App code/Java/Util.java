package com.dmi.meetingrecorder;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;



public class Util {

    public static byte[] getByteArrayFromUri(Intent result) {
        Uri data = result.getData();
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        FileInputStream fis;
        try {
            fis = new FileInputStream(new File(data.getPath()));
            byte[] buf = new byte[1024];
            int n;
            while (-1 != (n = fis.read(buf)))
                baos.write(buf, 0, n);
        } catch (Exception e) {
            e.printStackTrace();
        }
        byte[] bbytes = baos.toByteArray();
        return bbytes;
    }

    public static void shareOnMail(Context context, String path)
    {

    }
}
