import React, { useEffect, useState } from "react";
import style from "./index";
import {Keyboard,
        TouchableWithoutFeedback,
        View,
        Alert,
        Text,
        Image
    } from 'react-native';
import OTPInputView from '@twotalltotems/react-native-otp-input'
import { verification } from "@mokhta_s/react-statfive-api";
import { useNavigation } from "@react-navigation/native";



const VerificationScreen = () => {
    const navigation = useNavigation()

    const checkOtp = async (code) => {
        const result = await verification(code);

        if(result && result.data && result.data.error) {
            Alert.alert(
            "Erreur",
            result.data.message,
            [
                { text: "OK", onPress: () => console.log('Erreur', result.data.message) }
            ]
        );
        }
        else {
            navigation.navigate('Accueil')
        }
    }


    return (
        <TouchableWithoutFeedback style={style.containerView} onPress={Keyboard.dismiss}>
            <View style={style.boxOtp}>
                <Text style={style.titleText}>
                    Veuillez entrer le code reçu par mail pour confirmer votre compte
                </Text>
                <OTPInputView
                    style={{width: '100%', height: 150}}
                    pinCount={4}
                    autoFocusOnLoad
                    placeholderCharacter="0"
                    codeInputFieldStyle={style.underlineStyleBase}
                    codeInputHighlightStyle={style.underlineStyleHighLighted}
                    onCodeFilled = {(code => {
                        checkOtp(code)
                    })}
                />
            </View>       
        </TouchableWithoutFeedback>
    );
}

export default VerificationScreen;