package com.example.studex;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.annotation.NonNull;

import com.example.studex.fragments.ChatsFragment;
import com.example.studex.fragments.HomeFragment;
import com.example.studex.fragments.LoginFragment;
import com.example.studex.fragments.NewListingFragment;
import com.example.studex.fragments.ProfileFragment;
import com.example.studex.fragments.SearchFragment;
import com.google.android.material.bottomnavigation.BottomNavigationView;

import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Toast;

import androidx.appcompat.widget.Toolbar;
import androidx.fragment.app.Fragment;
import androidx.navigation.NavController;
import androidx.navigation.NavDestination;
import androidx.navigation.Navigation;
import androidx.navigation.fragment.NavHostFragment;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class MainActivity extends AppCompatActivity {
    private static final String baseURL = "https://studex.azurewebsites.net/";
    private static final List<Integer> logInReqFragments = Arrays.asList(R.id.newListingFragment, R.id.chatsFragment, R.id.profileFragment);
    private NavHostFragment navHostFragment;
    private static NavController navController;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        BottomNavigationView bottomNavigationView = findViewById(R.id.bottomnav);
        navHostFragment = (NavHostFragment) getSupportFragmentManager()
                .findFragmentById(R.id.navHostFragment);
        navController = navHostFragment.getNavController();

        navController.addOnDestinationChangedListener(new NavController.OnDestinationChangedListener() {
            @Override
            public void onDestinationChanged(@NonNull NavController navController,
                                             @NonNull NavDestination navDestination,
                                             @Nullable Bundle bundle) {
                if (logInReqFragments.contains(navDestination.getId())) {
                    if (!Authentication.isLoggedIn()) {
                        navController.navigate(R.id.loginFragment);
                    }
                }
            }
        });


        NavigationUI.setupWithNavController(bottomNavigationView, navController);



        Set<Integer> mainFragmentSet = new HashSet<>(Arrays.asList(R.id.homeFragment,
                R.id.searchFragment, R.id.newListingFragment, R.id.chatsFragment, R.id.profileFragment));

        AppBarConfiguration appBarConfiguration = new AppBarConfiguration.Builder(mainFragmentSet).build();
        Toolbar toolbar = findViewById(R.id.toolbar);
        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);
    }
    @Override
    public boolean onSupportNavigateUp() {
        return navController.navigateUp();
    }


    // ______________HANDLE TOP NAVIGATION BAR__________________
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.top_nav, menu);
        return true;
    }

    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        switch (id) {
            case R.id.logout_button:
                // do something
                return true;
        }

        return super.onOptionsItemSelected(item);
    }

    /*public void loadFragment(Fragment fragment) {
        //to attach fragment
        getSupportFragmentManager().beginTransaction().replace(R.id.relativelayout, fragment).commit();
    }*/

    public static String getBaseURL() {
        return baseURL;
    }
    public NavHostFragment getNavHostFragment() {
        return navHostFragment;
    }
    public static NavController getNavController() {
        return navController;
    }

}
// Points:
// TODO: Server-labbar
// TODO: Android-labbar
// TODO: Nav graph fullt ut
// TODO: (safe args)
// TODO: (kamera / GPS)
// TODO: (skriva chattar)
// TODO: (favoirtea listings)
// TODO: (safe args / extra rapport / )

// TODO:
// TODO: Göra om messages till Messages och inte Strings
// TODO: Bugg: Fixa No package ID 7f found for ID 0x7f07008d när man går till home page
// TODO: Använda navgraph
// TODO: Bugg: Register Fragment visar failed to register även om man registrerar sig successfully
// TODO: Change all of the hardcoded strings to be defined in the string.xml file instead (extract string)
// TODO: Clean up all of the ids of every object since refactoring changes stuff that shouldn't be changed
// TODO: (Set every longer text field (description for example) in a scroll view so the object will take up less space in the fragment)
// TODO: Update bottom navigation when redirected from log in
// TODO: Edit listing i listingFragment ska också vara send message ifall det inte är ens egen listing man kollar på
// TODO: Favorite i listingFragment ska också vara unfavorite ifall listingen redan är favorited
// TODO: ConstraintLayouten i chatFragment ska ta en till listingen då man klickar på den
// TODO: Sumbit knappen i newListingFragment ska ta en till ListingFragment där man ser Listingen??? no need for it men sku va coolt
// TODO: Code clean up (IDs, comments, )
// TODO:
// TODO:
// TODO:
// TODO:
// TODO:
// TODO:
// TODO:
// TODO:
// TODO:
