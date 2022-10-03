import React, { useState } from "react";
import style from "./index";
import {Keyboard,
        Text,
        View,
        TextInput,
        TouchableWithoutFeedback,
        Alert,
        KeyboardAvoidingView,
        Image,
        ScrollView,
        TouchableOpacity
    } from 'react-native';
import { register } from "@mokhta_s/react-statfive-api";
import { API_URL } from "../../../static";
import { useNavigation } from '@react-navigation/native';
import AsyncStorage from '@react-native-async-storage/async-storage';




const RegisterScreen = () => {
    const [password, setPassword] = useState("")
    const [email, setEmail] = useState("")
    const [firstname, setFirstname] = useState("")
    const [lastname, setLastname] = useState("")

    const navigation = useNavigation();

    const checkMail = (val) => {
        const regEmail = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (regEmail.test(val)) {
            return true;
        } else {
            return false;
        }
    }

    const onRegisterPress = async () => {
        if(checkMail(email)) {
            const result = await register(API_URL, email, firstname, lastname, password, password)
            if(result && result.error) {
                Alert.alert(
                    "Erreur",
                    result.message,
                    [
                        { text: "OK", onPress: () => console.log("Une erreur dans l'inscription est survenue") }
                    ]
                );
            } else {
                navigation.navigate('Login')
            }
        } else {
            Alert.alert(
                    "Erreur",
                    "L'email n'est pas conforme.",
                    [
                        { text: "OK", onPress: () => console.log("Une erreur dans l'inscription est survenue") }
                    ]
                );
        }
    }

    return (
        <TouchableWithoutFeedback style={style.containerView} onPress={Keyboard.dismiss}>
          <ScrollView style={style.ScrollView}>
            <KeyboardAvoidingView behavior="padding">
                <View style={style.registerScreenContainer}>
                    <View style={style.registerFormView}>
                        <Image
                          style={{width: '100%', height: 375}}
                          source={require('../../../public/StatFive.gif')}
                        />
                        <TextInput placeholder="Prénom" placeholderTextColor="#0090F8" style={style.registerFormTextInput} onChangeText={setFirstname} />
                        <TextInput placeholder="Nom" placeholderTextColor="#0090F8" style={style.registerFormTextInput} onChangeText={setLastname} />
                        <TextInput placeholder="E-mail" placeholderTextColor="#0090F8" style={style.registerFormTextInput} onChangeText={setEmail} />
                        <TextInput placeholder="Mot de Passe" placeholderTextColor="#0090F8" style={style.registerFormTextInput} secureTextEntry={true} onChangeText={setPassword} />
                        <View style={style.centerDiv}>
                            <TouchableOpacity
                            disabled={email.length < 1 || password.length < 1}
                            style={style.registerButton}
                            onPress={() => onRegisterPress()}
                            >
                                <Text style={style.registerButtonText}>Créer votre compte</Text>
                            </TouchableOpacity>    
                        </View>
                        <View style={style.MainContainer}>
                            <TouchableOpacity onPress={() => navigation.navigate('Login')}>
                                <Text style={style.TextStyle}>J'ai déjà un compte</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                </View>
            </KeyboardAvoidingView>
          </ScrollView>
        </TouchableWithoutFeedback>
    );
}

export default RegisterScreen;