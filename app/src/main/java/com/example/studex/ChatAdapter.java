package com.example.studex;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class ChatAdapter extends RecyclerView.Adapter<ChatAdapter.ChatViewHolder> {
    private List<ChatData> chats;

    public ChatAdapter(List<ChatData> chats) {
        this.chats = chats;
    }

    @Override
    public ChatViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.fragment_small_chat, parent, false);
        return new ChatViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(ChatViewHolder holder, int position) {
        ChatData chat = chats.get(position);
        ListingData listing = chat.getListing();
        holder.userTextView.setText(listing.getSeller());
        holder.listingTitleTextView.setText(listing.getTitle());

    }

    @Override
    public int getItemCount() {
        return chats.size();
    }

    public static class ChatViewHolder extends RecyclerView.ViewHolder {
        public TextView userTextView;
        public TextView listingTitleTextView;

        public ChatViewHolder(View itemView) {
            super(itemView);
            userTextView = itemView.findViewById(R.id.preview_user_text);
            listingTitleTextView = itemView.findViewById(R.id.preview_listing_title_text);

            View smallListing = itemView.findViewById(R.id.frameLayout7);
            smallListing.setOnClickListener(view2 ->{
                MainActivity.getNavController().navigate(R.id.chatFragment);

            });
        }
    }
}
