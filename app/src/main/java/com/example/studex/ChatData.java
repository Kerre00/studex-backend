package com.example.studex;

import android.graphics.Bitmap;

import androidx.annotation.Nullable;

import java.util.List;

public class ChatData {
    private List<String> messages;
    private ListingData listing;

    public ChatData(List<String> messages, ListingData listing) {
        this.messages = messages;
        this.listing = listing;
    }

    public List<String> getMessages() {
        return messages;
    }
    public ListingData getListing() {
        return listing;
    }

}
