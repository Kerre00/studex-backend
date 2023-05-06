package com.example.studex.fragments;

import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.studex.MainActivity;
import com.example.studex.R;
import com.example.studex.UserData;
import com.example.studex.databinding.FragmentRegistrationBinding;
import com.google.gson.Gson;
import com.google.gson.JsonArray;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link RegistrationFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class RegistrationFragment extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String userName;
    private String email;
    private String password;
    private String firstName;
    private String lastName;
    private String phoneNumber;


    public RegistrationFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment RegistrationFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static RegistrationFragment newInstance(String param1, String param2) {
        RegistrationFragment fragment = new RegistrationFragment();
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
            userName = getArguments().getString(ARG_PARAM1);
            email = getArguments().getString(ARG_PARAM2);
            password = getArguments().getString(ARG_PARAM1);
            firstName = getArguments().getString(ARG_PARAM2);
            lastName = getArguments().getString(ARG_PARAM1);
            phoneNumber = getArguments().getString(ARG_PARAM2);
        }
    }

    Button registerButton;
    Button cancelButton;
    FragmentRegistrationBinding binding;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        binding = FragmentRegistrationBinding.inflate(inflater, container, false);
        registerButton = binding.regButton;

        String url = MainActivity.getBaseURL() + "/signup";
        RequestQueue queue = Volley.newRequestQueue(getContext());

        // Register button click listener
        registerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Get the text from the EditTexts
                String userName = binding.usernameInput.getText().toString();
                String email = binding.emailInput.getText().toString();
                String password = binding.passwordInput.getText().toString();
                String firstName = binding.firstNameInput.getText().toString();
                String lastName = binding.lastNameInput.getText().toString();
                String phoneNumber = binding.phoneNumberInput.getText().toString();

                // Create a new User object
                UserData user = new UserData(userName, email, password, firstName, lastName, phoneNumber);

                // Convert the User object to JSON
                Gson gson = new Gson();
                String json = gson.toJson(user);

                JSONObject jsonRequest= null;
                try {
                    jsonRequest = new JSONObject(json);
                } catch (JSONException e) {
                    throw new RuntimeException(e);
                }

                // Create a new StringRequest
                String url = MainActivity.getBaseURL() + "signup";
                RequestQueue queue = Volley.newRequestQueue(getContext());

                JsonObjectRequest request = new JsonObjectRequest(Request.Method.POST, url, jsonRequest,
                        new Response.Listener<JSONObject>() {
                            @Override
                            public void onResponse(JSONObject response) {
                                // Handle the response
                                Toast.makeText(getContext(), "Registered", Toast.LENGTH_LONG).show();

                            }
                        }, new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError error) {
                                Toast.makeText(getContext(), "Failed to register", Toast.LENGTH_LONG).show();
                                // Log.i("Network Error", error.getMessage());
                            }
                        });

                queue.add(request);
            }
        });
        cancelButton = binding.regCancelButton;
        cancelButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                MainActivity.getNavController().navigateUp();
            }});

        return binding.getRoot();
    }
}
/*try {
                                    Toast.makeText(getContext(), "registered", Toast.LENGTH_SHORT).show();

                                    // Create a new RegisterFragment
                                    RegistrationFragment registerFragment = new RegistrationFragment();

                                    // Replace the current fragment with the RegisterFragment
                                    getActivity().getSupportFragmentManager().beginTransaction()
                                            .replace(R.id.relativelayout, registerFragment)
                                            .commit();

                                } catch (Exception e) {
                                    e.printStackTrace();
                                }*/