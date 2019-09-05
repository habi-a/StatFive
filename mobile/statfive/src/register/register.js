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

    onRegister() {
        let body = new FormData();
        body.append("email", this.state.email)
        body.append("firstname", this.state.firstname)
        body.append("lastname", this.state.lastname)
        body.append("password", this.state.password)
        body.append("c_password", this.state.c_password)
        const register = {
            method: 'POST',
            headers: {
                'Content-Type': 'multipart/form-data',
            },
            body: body,
        };
        if (annexe.checkInput1(this.state) == false) {
            Alert.alert(
                'Erreur',
                'Remplir tout les champs',
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
                            'ERREUR',
                        );
                        console.log(res)
                    } else {
                        Alert.alert(
                            'Félicitation!',
                            'Vous avez créer un compte.',
                        );
                        console.log(res.Firstame)
                        this.props.navigation.navigate('Accueil')
                    }
                }
            }).catch((error) => console.error("Erreur Register: " ,error));
        }
    }

  render() {
    return (
    <ImageBackground source={require('../../assets/background-home.png')} style={{width: '100%', height: '100%'}}>
        <KeyboardAvoidingView style={styles.containerView} behavior="padding">
            <ScrollView>
                <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
                    <View style={styles.registerScreenContainer}>
                        <View style={styles.registerFormView}>
                            <Text style={styles.logoText}>StatFive</Text>
                            <TextInput placeholder="Prénom" placeholderTextColor="#3897f1" style={styles.registerFormTextInput} onChange={(e) => this.setState({firstname: e.nativeEvent.text})} />
                            <TextInput placeholder="Nom" placeholderTextColor="#3897f1" style={styles.registerFormTextInput} onChange={(e) => this.setState({lastname: e.nativeEvent.text})} />
                            <TextInput placeholder="E-mail" placeholderTextColor="#3897f1" style={styles.registerFormTextInput} onChange={(e) => this.setState({email: e.nativeEvent.text})} />
                            <TextInput placeholder="Mot de Passe" placeholderTextColor="#3897f1" style={styles.registerFormTextInput} secureTextEntry={true} onChange={(e) => this.setState({password: e.nativeEvent.text})} />
                            <TextInput placeholder="Confirmation Mmot de Passe" placeholderTextColor="#3897f1" style={styles.registerFormTextInput} secureTextEntry={true} onChange={(e) => this.setState({c_password: e.nativeEvent.text})} />
                            <Button
                            buttonStyle={styles.RegisterButton}
                            onPress={() => this.onRegister()} title="Créer votre compte"
                            />
                            <View style={styles.MainContainer}>
                                <Text style={styles.TextStyle} onPress={ ()=> this.props.navigation.goBack() }>J'ai un compte</Text>
                            </View>
                        </View>
                    </View>
                </TouchableWithoutFeedback>
            </ScrollView>
        </KeyboardAvoidingView>
    </ImageBackground>
    )
  }
}