package com.example.studex.fragments;

import static com.example.studex.Authentication.getAccessTokenKey;

import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.example.studex.Authentication;
import com.example.studex.ListingData;
import com.example.studex.MainActivity;
import com.example.studex.R;
import com.example.studex.databinding.FragmentNewListingBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;


/**
 * A simple {@link Fragment} subclass.
 * Use the {@link NewListingFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class NewListingFragment extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    private Button getLocationBtn;
    private Button openCameraBtn;
    private Button openGalleryBtn;
    private Button SubmitBtn;
    private Button CancelBtn;

    private String token;
    private String title;
    private String price;
    private String location;
    private String description;


    public NewListingFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment NewListingFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static NewListingFragment newInstance(String param1, String param2) {
        NewListingFragment fragment = new NewListingFragment();
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

    FragmentNewListingBinding binding;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        binding = FragmentNewListingBinding.inflate(inflater, container, false);
        getLocationBtn = binding.getLocationButton;
        openCameraBtn = binding.openCameraButton;
        openGalleryBtn = binding.addPictureButton;
        SubmitBtn = binding.submitPostButton;
        CancelBtn = binding.cancelPostButton;

        getLocationBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });

        openCameraBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });

        openGalleryBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });

        SubmitBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String title = binding.titleField.getText().toString();
                String location = binding.locationField.getText().toString();
                String description = binding.descriptionField.getText().toString();
                String price = binding.priceField.getText().toString();
                /*String seller = binding.sellerField.getText().toString();*/
                String seller = "Fake User";

                if (price.contains(",")) {
                    price = price.replace(",", ".");
                }

                Float floatPrice = null;
                try {
                    floatPrice = Float.parseFloat(price);
                } catch (NumberFormatException e) {
                    Toast.makeText(getContext(), "Price must be a number", Toast.LENGTH_SHORT).show();
                    return;
                }

                // Create a new listing object
                ListingData listing = new ListingData(title, floatPrice, description, location, seller, null);

                // Convert the User object to JSON
                Gson gson = new Gson();
                String json = gson.toJson(listing);

                JSONObject jsonRequest = null;
                try {
                    jsonRequest = new JSONObject(json);
                } catch (JSONException e) {
                    throw new RuntimeException(e);
                }

                // Create a new StringRequest
                String url = MainActivity.getBaseURL() + "listing/add";
                RequestQueue queue = Volley.newRequestQueue(getContext());

                // Send the request
                JsonObjectRequest request = new JsonObjectRequest(Request.Method.POST, url, jsonRequest,
                        new Response.Listener<JSONObject>() {
                            @Override
                            public void onResponse(JSONObject response) {
                                Toast.makeText(getContext(), "Listing added successfully", Toast.LENGTH_SHORT).show();

                                /*ProfileFragment profileFragment = new ProfileFragment();
                                getActivity().getSupportFragmentManager().beginTransaction()
                                        .replace(R.id.relativelayout, profileFragment)
                                        .commit();*/
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(getContext(), "Error adding listing", Toast.LENGTH_SHORT).show();
                    }
                }){
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    Map<String, String> headers = new HashMap<>();
                    headers.put("Authorization", "Bearer " + getAccessTokenKey());
                    headers.put("Content-Type", "application/json");
                    return headers;
                }};

                queue.add(request);
            }
        });

        CancelBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                /*HomeFragment homeFragment = new HomeFragment();
                getActivity().getSupportFragmentManager().beginTransaction()
                        .replace(R.id.relativelayout, homeFragment)
                        .commit();*/
            }
        });



        return binding.getRoot();
    }
}