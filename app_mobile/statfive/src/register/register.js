import React, { Component } from "react";
import styles from "./style";
import {Keyboard,
        Text,
        Alert,
        View,
        TextInput,
        TouchableWithoutFeedback,
        KeyboardAvoidingView,
        ImageBackground} from 'react-native';
import { Button } from 'react-native-elements';
import { ScrollView } from "react-native-gesture-handler";

import annexe from '../../annexe.js';

export default class RegisterScreen extends Component {

    static navigationOptions = {
        header:null,
      };

    constructor(props){
        super(props)
        this.state = {
          lastname: "",
          firstname: "",
          password: "",
          c_password: "",
          email: ""
        }
    }

    onRegisterPress = async () => {
        let body_register = new FormData();
        body_register.append("email", this.state.email)
        body_register.append("firstname", this.state.firstname)
        body_register.append("lastname", this.state.lastname)
        body_register.append("password", this.state.password)
        body_register.append("c_password", this.state.c_password)
        const register = {
            method: "POST",
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data',
            body:body_register,
        };
        if (annexe.checkInput1(this.state) == false) {
            Alert.alert(
              'Champs manquants',
              'Veuillez remplir tout les champs',
            );
        }
        else {
            fetch(annexe.ip+"addUser", register)
            .then(res => res.json())
            .then(res => {
                if(res.about == "Mail exist") {
                    Alert.alert(
                        'Erreur',
                        'Email déjà utilisé!!',
                    );
                } else {
                    if (res.error) {
                        Alert.alert(
                            'Erreur!',
                            'Une erreur est survenue',
                        );
                        console.log(res)
                    } else {
                        Alert.alert(
                            'Félicitation !',
                            'Vous avez créer un compte.',
                        );
                        this.props.navigation.navigate('Accueil')
                    }
                }
            }).catch((error) => console.error("Erreur Register: " ,error));
        };
    };

  render() {
    return (
    <ImageBackground source={require('../../assets/home.png')} style={{width: '100%', height: '100%'}}>
        <TouchableWithoutFeedback style={styles.containerView} onPress={Keyboard.dismiss}>
            <ScrollView>
            <KeyboardAvoidingView behavior="padding">
                <View style={styles.registerScreenContainer}>
                    <View style={styles.registerFormView}>
                        <Text style={styles.logoText}>StatFive</Text>
                        <TextInput placeholder="Prénom" placeholderTextColor="#196F3D" style={styles.registerFormTextInput} onChange={(e) => this.setState({firstname: e.nativeEvent.text})} />
                        <TextInput placeholder="Nom" placeholderTextColor="#196F3D" style={styles.registerFormTextInput} onChange={(e) => this.setState({lastname: e.nativeEvent.text})} />
                        <TextInput placeholder="E-mail" placeholderTextColor="#196F3D" style={styles.registerFormTextInput} onChange={(e) => this.setState({email: e.nativeEvent.text})} />
                        <TextInput placeholder="Mot de Passe" placeholderTextColor="#196F3D" style={styles.registerFormTextInput} secureTextEntry={true} onChange={(e) => this.setState({password: e.nativeEvent.text})} />
                        <TextInput placeholder="Confirmation Mot de Passe" placeholderTextColor="#196F3D" style={styles.registerFormTextInput} secureTextEntry={true} onChange={(e) => this.setState({c_password: e.nativeEvent.text})} />
                        <Button
                        buttonStyle={styles.registerButton}
                        onPress={() => this.onRegisterPress()}
                        title="Créer votre compte"
                        />
                        <View style={styles.MainContainer}>
                            <Text style={styles.TextStyle} onPress={ ()=> this.props.navigation.goBack() }>J'ai un compte</Text>
                        </View>
                    </View>
                </View>
            </KeyboardAvoidingView>
            </ScrollView>
        </TouchableWithoutFeedback>
    </ImageBackground>
    )
  }
}
