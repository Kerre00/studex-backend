package com.example.studex.fragments;

import android.content.res.Resources;
import android.graphics.BitmapFactory;
import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.example.studex.ListingAdapter;
import com.example.studex.ListingData;
import com.example.studex.R;

import java.util.ArrayList;
import java.util.List;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link HomeFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class HomeFragment extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER

    // TODO: Rename and change types of parameters
    private RecyclerView recyclerView;
    private ListingAdapter listingAdapter;
    public HomeFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @return A new instance of fragment HomeFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static HomeFragment newInstance() {
        HomeFragment fragment = new HomeFragment();
        Bundle args = new Bundle();
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_home, container, false);
//        loadFragment(new SmallListingFragment());
        // Find and initialize the RecyclerView
        recyclerView = view.findViewById(R.id.earlier_searches_content);
        recyclerView.setLayoutManager(new LinearLayoutManager(getActivity(), LinearLayoutManager.HORIZONTAL, false));
        // Create and set the adapter for the RecyclerView
        List<ListingData> Earlier_Searches_Listings = new ArrayList<>();
        Earlier_Searches_Listings.add(new ListingData("Post 1", 320.0f, "Description", "Linköping", "User1", BitmapFactory.decodeResource(Resources.getSystem(), R.drawable.ic_launcher_background)));
        Earlier_Searches_Listings.add(new ListingData("Post 2", 320.0f, "Description", "Linköping", "User2", BitmapFactory.decodeResource(Resources.getSystem(), R.mipmap.ic_launcher)));
        Earlier_Searches_Listings.add(new ListingData("Post 3", 320.0f, "Description", "Linköping", "User3", null));
        Earlier_Searches_Listings.add(new ListingData("Post 4", (float) 20, "Description", "Linköping", "User4", null));
        Earlier_Searches_Listings.add(new ListingData("Post 5", (float) 20, "Description", "Linköping", "User5", null));
        Earlier_Searches_Listings.add(new ListingData("Post 6", (float) 20, "Description", "Linköping", "User6", null));
        Earlier_Searches_Listings.add(new ListingData("Post 7", (float) 20, "Description", "Linköping", "User7", null));
        Earlier_Searches_Listings.add(new ListingData("Post 8", (float) 20, "Description", "Linköping", "User8", null));
        Earlier_Searches_Listings.add(new ListingData("Post 9", (float) 20, "Description", "Linköping", "User9", null));
        Earlier_Searches_Listings.add(new ListingData("Post 10", (float) 20, "Description", "Linköping", "User10", null));
        listingAdapter = new ListingAdapter(Earlier_Searches_Listings);

        recyclerView.setAdapter(listingAdapter);

        // Find and initialize the RecyclerView
        recyclerView = view.findViewById(R.id.new_posts_content);
        recyclerView.setLayoutManager(new LinearLayoutManager(getActivity(), LinearLayoutManager.HORIZONTAL, false));

        // Create and set the adapter for the RecyclerView
        List<ListingData> New_Listings = new ArrayList<>();
        New_Listings.add(new ListingData("Post 1", (float) 20, "Description", "Linköping", "User11", null));
        New_Listings.add(new ListingData("Post 2", (float) 20, "Description", "Linköping", "User12", null));
        New_Listings.add(new ListingData("Post 3", (float) 20, "Description", "Linköping", "User13", null));
        New_Listings.add(new ListingData("Post 4", (float) 20, "Description", "Linköping", "User14", null));
        New_Listings.add(new ListingData("Post 5", (float) 20, "Description", "Linköping", "User15", null));
        New_Listings.add(new ListingData("Post 6", (float) 20, "Description", "Linköping", "User16", null));
        New_Listings.add(new ListingData("Post 7", (float) 20, "Description", "Linköping", "User17", null));
        New_Listings.add(new ListingData("Post 8", (float) 20, "Description", "Linköping", "User18", null));
        New_Listings.add(new ListingData("Post 9", (float) 20, "Description", "Linköping", "User19", null));
        New_Listings.add(new ListingData("Post 10", (float) 20, "Description", "Linköping", "User20", null));
        listingAdapter = new ListingAdapter(New_Listings);

        recyclerView.setAdapter(listingAdapter);

        // Find and initialize the RecyclerView
        recyclerView = view.findViewById(R.id.favorite_posts_content);
        recyclerView.setLayoutManager(new LinearLayoutManager(getActivity(), LinearLayoutManager.HORIZONTAL, false));

        // Create and set the adapter for the RecyclerView
        List<ListingData> Favorite_Listings = new ArrayList<>();
        Favorite_Listings.add(new ListingData("Post 1", (float) 20, "Description", "Linköping", "User21", null));
        Favorite_Listings.add(new ListingData("Post 2", (float) 20, "Description", "Linköping", "User22", null));
        Favorite_Listings.add(new ListingData("Post 3", (float) 20, "Description", "Linköping", "User23", null));
        Favorite_Listings.add(new ListingData("Post 4", (float) 20, "Description", "Linköping", "User24", null));
        Favorite_Listings.add(new ListingData("Post 5", (float) 20, "Description", "Linköping", "User25", null));
        Favorite_Listings.add(new ListingData("Post 6", (float) 20, "Description", "Linköping", "User26", null));
        Favorite_Listings.add(new ListingData("Post 7", (float) 20, "Description", "Linköping", "User27", null));
        Favorite_Listings.add(new ListingData("Post 8", (float) 20, "Description", "Linköping", "User28", null));
        Favorite_Listings.add(new ListingData("Post 9", (float) 20, "Description", "Linköping", "User29", null));
        Favorite_Listings.add(new ListingData("Post 10", (float) 20, "Description", "Linköping", "User30", null));
        listingAdapter = new ListingAdapter(Favorite_Listings);

        recyclerView.setAdapter(listingAdapter);

        // Find and initialize the RecyclerView
        recyclerView = view.findViewById(R.id.unviewed_posts_content);
        recyclerView.setLayoutManager(new LinearLayoutManager(getActivity(), LinearLayoutManager.HORIZONTAL, false));

        // Create and set the adapter for the RecyclerView
        List<ListingData> Unviewed_Listings = new ArrayList<>();
        Unviewed_Listings.add(new ListingData("Post 1", (float) 20, "Description", "Linköping", "User31", null));
        Unviewed_Listings.add(new ListingData("Post 2", (float) 20, "Description", "Linköping", "User32", null));
        Unviewed_Listings.add(new ListingData("Post 3", (float) 20, "Description", "Linköping", "User33", null));
        Unviewed_Listings.add(new ListingData("Post 4", (float) 20, "Description", "Linköping", "User34", null));
        Unviewed_Listings.add(new ListingData("Post 5", (float) 20, "Description", "Linköping", "User35", null));
        Unviewed_Listings.add(new ListingData("Post 6", (float) 20, "Description", "Linköping", "User36", null));
        Unviewed_Listings.add(new ListingData("Post 7", (float) 20, "Description", "Linköping", "User37", null));
        Unviewed_Listings.add(new ListingData("Post 8", (float) 20, "Description", "Linköping", "User38", null));
        Unviewed_Listings.add(new ListingData("Post 9", (float) 20, "Description", "Linköping", "User39", null));
        Unviewed_Listings.add(new ListingData("Post 10", (float) 20, "Description", "Linköping", "User40", null));
        listingAdapter = new ListingAdapter(Unviewed_Listings);

        recyclerView.setAdapter(listingAdapter);

        // Find and initialize the RecyclerView
        recyclerView = view.findViewById(R.id.filtered_posts_content);
        recyclerView.setLayoutManager(new LinearLayoutManager(getActivity(), LinearLayoutManager.HORIZONTAL, false));

        // Create and set the adapter for the RecyclerView
        List<ListingData> Filtered_Listings = new ArrayList<>();
        Filtered_Listings.add(new ListingData("Post 1", (float) 20, "Description", "Linköping", "User41", null));
        Filtered_Listings.add(new ListingData("Post 2", (float) 20, "Description", "Linköping", "User42", null));
        Filtered_Listings.add(new ListingData("Post 3", (float) 20, "Description", "Linköping", "User43", null));
        Filtered_Listings.add(new ListingData("Post 4", (float) 20, "Description", "Linköping", "User44", null));
        Filtered_Listings.add(new ListingData("Post 5", (float) 20, "Description", "Linköping", "User45", null));
        Filtered_Listings.add(new ListingData("Post 6", (float) 20, "Description", "Linköping", "User46", null));
        Filtered_Listings.add(new ListingData("Post 7", (float) 20, "Description", "Linköping", "User47", null));
        Filtered_Listings.add(new ListingData("Post 8", (float) 20, "Description", "Linköping", "User48", null));
        Filtered_Listings.add(new ListingData("Post 9", (float) 20, "Description", "Linköping", "User49", null));
        Filtered_Listings.add(new ListingData("Post 10", (float) 20, "Description", "Linköping", "User50", null));
        listingAdapter = new ListingAdapter(Filtered_Listings);

        recyclerView.setAdapter(listingAdapter);

        // Find and initialize the RecyclerView
        recyclerView = view.findViewById(R.id.for_you_content);
        GridLayoutManager gridLayoutManager = new GridLayoutManager(getActivity(), 2);
        recyclerView.setLayoutManager(gridLayoutManager);

        // Create and set the adapter for the RecyclerView
        List<ListingData> Listings = new ArrayList<>();
        Listings.add(new ListingData("Post 1", (float) 20, "Description", "Linköping", "User51", null));
        Listings.add(new ListingData("Post 2", (float) 20, "Description", "Linköping", "User52", null));
        Listings.add(new ListingData("Post 3", (float) 20, "Description", "Linköping", "User53", null));
        Listings.add(new ListingData("Post 4", (float) 20, "Description", "Linköping", "User54", null));
        Listings.add(new ListingData("Post 5", (float) 20, "Description", "Linköping", "User55", null));
        Listings.add(new ListingData("Post 6", (float) 20, "Description", "Linköping", "User56", null));
        Listings.add(new ListingData("Post 7", (float) 20, "Description", "Linköping", "User57", null));
        Listings.add(new ListingData("Post 8", (float) 20, "Description", "Linköping", "User58", null));
        Listings.add(new ListingData("Post 9", (float) 20, "Description", "Linköping", "User59", null));
        Listings.add(new ListingData("Post 10", (float) 20, "Description", "Linköping", "User60", null));
        listingAdapter = new ListingAdapter(Listings);

        recyclerView.setAdapter(listingAdapter);

        return view;
    }

}