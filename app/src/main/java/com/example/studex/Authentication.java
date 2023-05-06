package com.example.studex;

import android.content.Context;
import android.content.SharedPreferences;

import com.android.volley.AuthFailureError;

import java.util.HashMap;
import java.util.Map;

public class Authentication {
    /*private static String ACCESS_TOKEN_KEY = "access_token";*/
    private static String ACCESS_TOKEN_KEY = "valid_token";
    private static SharedPreferences preferences;
    private boolean isOnline = false;
    private static String username;

    public Authentication(Context context) {
        preferences = context.getSharedPreferences("my_app", Context.MODE_PRIVATE);
    }

    public void saveAccessToken(String token) {
        SharedPreferences.Editor editor = preferences.edit();
        editor.putString(ACCESS_TOKEN_KEY, token);
        editor.apply();
    }

    public static String getAccessToken() {
        return preferences.getString(ACCESS_TOKEN_KEY, null);
    }
    public static void setAccessToken(String accessToken) {
        try {
            SharedPreferences.Editor editor = preferences.edit();
            editor.putString(ACCESS_TOKEN_KEY, accessToken);
            editor.apply();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void clearAccessToken() {
        preferences.edit().remove(ACCESS_TOKEN_KEY).apply();
    }
    public static boolean isLoggedIn() {
        return ACCESS_TOKEN_KEY != "access_token";
    }

    public static void setAccessTokenKey(String accessTokenKey) {
        ACCESS_TOKEN_KEY = accessTokenKey;
    }

    public static String getAccessTokenKey() {
        return ACCESS_TOKEN_KEY;
    }

    public static Boolean setOnlineStatus(boolean status) {
        return status;
    }

    public static String getUsername() {
        return username;
    }
    public static void setUsername(String username) {
        Authentication.username = username;
    }


}
