package com.example.studex;

import android.graphics.Bitmap;

import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.Nullable;

import java.util.Map;

public class ListingData {
    private String title;
    private String description;
    private Float price;
    private String location;
    private String seller;
    private Bitmap image;
    public ListingData(String title, Float price, String description, String location, String seller, @Nullable Bitmap image) {
        this.title = title;
        this.description = description;
        this.price = price;
        this.location = location;
        this.seller = seller;
        this.image = image;
    }

    public String getTitle() {
        return title;
    }
    public String getPrice() {
        return price.toString();
    }
    public String getDescription() {
        return description;
    }
    public String getLocation() {
        return location;
    }
    public String getSeller() {
        return seller;
    }
    public Bitmap getImage() {
        return image;
    }

}
