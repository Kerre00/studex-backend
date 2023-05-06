package com.example.studex.fragments;

import android.app.Activity;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.navigation.NavController;
import androidx.navigation.NavDestination;
import androidx.navigation.Navigation;
import androidx.navigation.fragment.NavHostFragment;
import androidx.navigation.ui.NavigationUI;


import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import com.example.studex.R;
import com.google.android.material.bottomnavigation.BottomNavigationView;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link ProfileFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class ProfileFragment extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;


    public ProfileFragment() {
        // Required empty public constructor

    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment ProfileFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static ProfileFragment newInstance(String param1, String param2) {
        ProfileFragment fragment = new ProfileFragment();
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
        View view = inflater.inflate(R.layout.fragment_profile, container, false);
        Button credentialsButton = view.findViewById(R.id.credentials_button);
        credentialsButton.setOnClickListener(view2 ->{
            NavController navController = Navigation.findNavController(getActivity(), R.id.navHostFragment2);
            NavDestination currentDestination = navController.getCurrentDestination();

            if (currentDestination.getId() == R.id.noDisplay) {
                navController.navigate(R.id.action_noDisplay_to_credentialsFragment);
            } else if (currentDestination.getId() == R.id.credentialsFragment) {

            } else {
                navController.navigate(R.id.action_listingsFragment_to_credentialsFragment);
            }
        });
        Button yourListingsButton = view.findViewById(R.id.listings_button);
        yourListingsButton.setOnClickListener(view2 ->{
            NavController navController = Navigation.findNavController(getActivity(), R.id.navHostFragment2);
            NavDestination currentDestination = navController.getCurrentDestination();

                if (currentDestination.getId() == R.id.noDisplay) {
                    navController.navigate(R.id.action_noDisplay_to_listingsFragment);
                } else if (currentDestination.getId() == R.id.listingsFragment) {

                } else {
                    navController.navigate(R.id.action_credentialsFragment_to_listingsFragment);
                }
        });
        return view;
    }
}