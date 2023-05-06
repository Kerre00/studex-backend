package com.example.studex.fragments;

import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.example.studex.Authentication;
import com.example.studex.MainActivity;
import com.example.studex.R;
import com.example.studex.UserData;
import com.example.studex.databinding.FragmentLoginBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link LoginFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class LoginFragment extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String username;
    private String password;
    private Button loginButton;
    private Button registerButton;

    public LoginFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment LoginFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static LoginFragment newInstance(String param1, String param2) {
        LoginFragment fragment = new LoginFragment();
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
            username = getArguments().getString(ARG_PARAM1);
            password = getArguments().getString(ARG_PARAM2);
        }
    }

    FragmentLoginBinding binding;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        binding = FragmentLoginBinding.inflate(inflater, container, false);

        registerButton = binding.createAccountButton;
        loginButton = binding.buttonSignIn;

        loginButton.setOnClickListener(new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            String userName = binding.usernameField.getText().toString();
            String password = binding.passwordField.getText().toString();

            // Create a new User object
            UserData user = new UserData(userName, password);

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
            String url = MainActivity.getBaseURL() + "login";
            RequestQueue queue = Volley.newRequestQueue(getContext());

            // Send the request
            JsonObjectRequest request = new JsonObjectRequest(Request.Method.POST, url, jsonRequest,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            // Handle the response
                            try {
                                String token = response.getString("token");
                                Authentication.setAccessTokenKey(token);
                                System.out.println(Authentication.getAccessTokenKey() + "---------------------------------------------------------------------------------");
                                Authentication.setUsername(userName);
                                Toast.makeText(getContext(), "Login successful", Toast.LENGTH_SHORT).show();
                                // Create a new RegisterFragment
                                HomeFragment homeFragment = new HomeFragment();

                                // Replace the current fragment with the RegisterFragment
                                /*getActivity().getSupportFragmentManager().beginTransaction()
                                        .replace(R.id.relativelayout, homeFragment)
                                        .commit();*/

                            } catch (JSONException e) {
                                throw new RuntimeException(e);
                            }
                        }
                    }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    // Handle the error
                    Toast.makeText(getContext(), "Login failed", Toast.LENGTH_SHORT).show();
                }
            });
        queue.add(request);
        }
        });

        registerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                MainActivity.getNavController().navigate(R.id.action_loginFragment_to_registrationFragment);
            }
        });

        // Inflate the layout for this fragment
        return binding.getRoot();
    }
}