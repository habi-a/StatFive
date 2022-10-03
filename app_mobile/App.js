import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

import LoginScreen from "./src/components/login/Login";
import RegisterScreen from "./src/components/register/Register";
import VerificationScreen from "./src/components/verification/Verification";
import AccueilScreen from "./src/components/accueil/Accueil";
import StatisticScreen from "./src/components/statistique/Statistique";
import ProfilScreen from "./src/components/profil/Profil";
import ClassementScreen from "./src/components/classement/Classement";

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen
          name="Login"
          component={LoginScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Register"
          component={RegisterScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Verification"
          component={VerificationScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Accueil"
          component={AccueilScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Statistic"
          component={StatisticScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Profil"
          component={ProfilScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Classement"
          component={ClassementScreen}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
