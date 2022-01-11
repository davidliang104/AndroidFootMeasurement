package com.example.footmeasurement;

import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import org.w3c.dom.Text;

import java.io.ByteArrayOutputStream;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }

        // Get bitmap of image
        Drawable drawable = getResources().getDrawable(R.drawable.foot3);
        Bitmap bitmap= ((BitmapDrawable)drawable).getBitmap();
        // Convert bitmap to byte array
        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, stream);
        byte[] imageInByte = stream.toByteArray();

        Python py = Python.getInstance();
        PyObject module = py.getModule("main");
        String result = module.callAttr("main",imageInByte).toString();


        TextView t = findViewById(R.id.textView);
        t.setText(result);

    }
}