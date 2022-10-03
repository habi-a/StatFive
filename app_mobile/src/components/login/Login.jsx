import React, { useState } from "react";
import style from "./index";
import {Keyboard,
        Text,
        View,
        TextInput,
        TouchableWithoutFeedback,
        KeyboardAvoidingView,
        Image,
        SafeAreaView,
        Alert,
        TouchableOpacity} from 'react-native';
import { API_URL } from "../../../static";
import { login } from "@mokhta_s/react-statfive-api"
import { useNavigation } from "@react-navigation/native";

const LoginScreen = () => {
    const [password, setPassword] = useState("")
    const [email, setEmail] = useState("")

    const navigation = useNavigation()

    const onLoginPress = async () => {
        const result = await login(API_URL, email, password)
        console.log('result', result, process.env.API_URL)
        if(result === "L'email n'est pas conforme.") {
            Alert.alert(
            "Erreur",
            result,
            [
                { text: "OK", onPress: () => setEmail('') }
            ]
        );
        }
        if(result?.data?.error) {
            Alert.alert(
            "Erreur",
            result.data.message,
            [
                { text: "OK", onPress: () => console.log("Une erreur dans l'inscription est survenue") }
            ]
        );
        } else {
            if(result?.data?.verification) {
                navigation.navigate('Accueil')
            } else {
                navigation.navigate('Verification')
            }
        }
    }

    return (
        <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
            <KeyboardAvoidingView style={style.containerView} behavior="padding">
                <View style={style.loginScreenContainer}>
                    <View style={style.loginFormView}>
                        <Image
                          style={{width: '100%', height: 360, marginBottom: -50}}
                          resizeMode="contain"
                          source={require('../../../public/StatFive.gif')}
                        />
                        <SafeAreaView>
                            <TextInput placeholder="E-mail" placeholderTextColor="#0090F8" value={email} style={style.loginFormTextInput} onChangeText={setEmail} />
                            <TextInput placeholder="Mot de Passe" placeholderTextColor="#0090F8" value={password} style={style.loginFormTextInput} secureTextEntry={true} onChangeText={setPassword} />
                        </SafeAreaView>

                        <View style={style.centerDiv}>
                            <TouchableOpacity
                            disabled={email.length < 1 || password.length < 1}
                            onPress={() => onLoginPress()}
                            style={style.loginButton}
                            >
                                <Text style={style.loginButtonText}>Connexion</Text>
                            </TouchableOpacity>    
                        </View>
                        
                        <View style={style.MainContainer}>
                            <TouchableOpacity onPress={() => navigation.navigate('Register')}>
                                <Text style={style.TextStyle}>Toujours pas inscrit ?</Text>
                            </TouchableOpacity>
                            
                        </View>
                    </View>
                </View>
            </KeyboardAvoidingView>
        </TouchableWithoutFeedback>
    );
}

export default LoginScreen;