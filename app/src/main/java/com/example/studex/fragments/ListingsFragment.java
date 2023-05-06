package com.example.studex.fragments;

import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.GridLayoutManager;
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
 * Use the {@link ListingsFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class ListingsFragment extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;
    private RecyclerView recyclerView;
    private ListingAdapter listingAdapter;

    public ListingsFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment ListingsFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static ListingsFragment newInstance(String param1, String param2) {
        ListingsFragment fragment = new ListingsFragment();
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
        View view = inflater.inflate(R.layout.fragment_listings, container, false);

        recyclerView = view.findViewById(R.id.listings_view);
        GridLayoutManager gridLayoutManager = new GridLayoutManager(getActivity(), 2);
        recyclerView.setLayoutManager(gridLayoutManager);

        // Create and set the adapter for the RecyclerView
        List<ListingData> Listings = new ArrayList<>();
        Listings.add(new ListingData("Post 1", (float) 20, "Description", "Linköping", "User1", null));
        Listings.add(new ListingData("Post 2", (float) 20, "Description", "Linköping", "User2", null));
        Listings.add(new ListingData("Post 3", (float) 20, "Description", "Linköping", "User3", null));
        Listings.add(new ListingData("Post 4", (float) 20, "Description", "Linköping", "User4", null));
        Listings.add(new ListingData("Post 5", (float) 20, "Description", "Linköping", "User5", null));
        Listings.add(new ListingData("Post 6", (float) 20, "Description", "Linköping", "User6", null));
        Listings.add(new ListingData("Post 7", (float) 20, "Description", "Linköping", "User7", null));
        Listings.add(new ListingData("Post 8", (float) 20, "Description", "Linköping", "User8", null));
        Listings.add(new ListingData("Post 9", (float) 20, "Description", "Linköping", "User9", null));
        Listings.add(new ListingData("Post 10", (float) 20, "Description", "Linköping", "User10", null));
        listingAdapter = new ListingAdapter(Listings);

        recyclerView.setAdapter(listingAdapter);
        return view;
    }

    /**
     * A simple {@link Fragment} subclass.
     * Use the {@link NoDisplay#newInstance} factory method to
     * create an instance of this fragment.
     */
    public static class NoDisplay extends Fragment {

        // TODO: Rename parameter arguments, choose names that match
        // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
        private static final String ARG_PARAM1 = "param1";
        private static final String ARG_PARAM2 = "param2";

        // TODO: Rename and change types of parameters
        private String mParam1;
        private String mParam2;

        public NoDisplay() {
            // Required empty public constructor
        }

        /**
         * Use this factory method to create a new instance of
         * this fragment using the provided parameters.
         *
         * @param param1 Parameter 1.
         * @param param2 Parameter 2.
         * @return A new instance of fragment NoDisplay.
         */
        // TODO: Rename and change types and number of parameters
        public static NoDisplay newInstance(String param1, String param2) {
            NoDisplay fragment = new NoDisplay();
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
            return inflater.inflate(R.layout.fragment_no_display, container, false);
        }
    }
}