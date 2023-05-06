package com.example.studex.fragments;

import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.example.studex.ChatAdapter;
import com.example.studex.ChatData;
import com.example.studex.ListingAdapter;
import com.example.studex.ListingData;
import com.example.studex.R;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link ChatsFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class ChatsFragment extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;
    private RecyclerView recyclerView;
    private ChatAdapter chatAdapter;

    public ChatsFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment ChatsFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static ChatsFragment newInstance(String param1, String param2) {
        ChatsFragment fragment = new ChatsFragment();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_chats, container, false);

        recyclerView = view.findViewById(R.id.chats_view);
        GridLayoutManager gridLayoutManager = new GridLayoutManager(getActivity(), 1);
        recyclerView.setLayoutManager(gridLayoutManager);

        // Create and set the adapter for the RecyclerView
        List<ChatData> chats = new ArrayList<>();
        ListingData listing1 = new ListingData("Post 1", (float) 20, "Description", "Linköping", "User1", null);
        ListingData listing2 = new ListingData("Post 2", (float) 20, "Description", "Linköping", "User2", null);
        ListingData listing3 = new ListingData("Post 3", (float) 20, "Description", "Linköping", "User3", null);
        ListingData listing4 = new ListingData("Post 4", (float) 20, "Description", "Linköping", "User4", null);
        ListingData listing5 = new ListingData("Post 5", (float) 20, "Description", "Linköping", "User5", null);

        List<String> messages1 = Arrays.asList("Hi", "Whats up", "Nothing much, you?");
        List<String> messages2 = Arrays.asList("Hello, can I buy your book?", "Sure, when?");
        List<String> messages3 = Arrays.asList("Can i buy your book for 200kr?", "That's too low", "Screw You");

        chats.add(new ChatData(messages1, listing1));
        chats.add(new ChatData(messages2, listing2));
        chats.add(new ChatData(messages3, listing3));
        chatAdapter = new ChatAdapter(chats);

        recyclerView.setAdapter(chatAdapter);
        return view;
    }
}