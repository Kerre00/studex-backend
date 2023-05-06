package com.example.studex;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.fragment.NavHostFragment;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class ListingAdapter extends RecyclerView.Adapter<ListingAdapter.ListingViewHolder> {
    private List<ListingData> listings;

    public ListingAdapter(List<ListingData> posts) {
        this.listings = posts;
    }

    @Override
    public ListingViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.fragment_small_listing, parent, false);
        return new ListingViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(ListingViewHolder holder, int position) {
        ListingData listing = listings.get(position);
        holder.textTextView.setText(listing.getTitle());
        holder.priceTextView.setText(listing.getPrice());
        if (listing.getImage() != null) {
            holder.photoImageView.setImageBitmap(listing.getImage());
        } else {
            holder.photoImageView.setImageResource(R.drawable.ic_no_image);
        }
    }

    @Override
    public int getItemCount() {
        return listings.size();
    }

    public static class ListingViewHolder extends RecyclerView.ViewHolder {
        public TextView textTextView;
        public ImageView photoImageView;
        public TextView priceTextView;

        public ListingViewHolder(View itemView) {
            super(itemView);
            textTextView = itemView.findViewById(R.id.small_listing_title);
            photoImageView = itemView.findViewById(R.id.small_listing_image);
            priceTextView = itemView.findViewById(R.id.small_listing_price);

            View smallListing = itemView.findViewById(R.id.frameLayout19);
            smallListing.setOnClickListener(view2 ->{
                MainActivity.getNavController().navigate(R.id.listingFragment);

            });
        }
    }
}
