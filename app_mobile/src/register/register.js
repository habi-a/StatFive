import React, { Component } from "react";
import { createStackNavigator } from 'react-navigation-stack';
import { createAppContainer } from 'react-navigation';
import {Keyboard,
        Text,
        View,
        TextInput,
        TouchableWithoutFeedback,
        Alert,
        KeyboardAvoidingView,
        Image,
        ImageBackground} from 'react-native';
import { Button } from 'react-native-elements';
import { ScrollView } from "react-native-gesture-handler";

import style from "./style";
import annexe from '../../api_link'

TextInput.defaultProps.selectionColor = '#0090F8'

export default class RegisterScreen extends Component {

    static navigationOptions = {
        headerShown:false,
      };

    constructor(props){
        super(props)
        this.state = {
          lastname: "",
          firstname: "",
          password: "",
          email: ""
        }
    }

    onRegisterPress = async () => {
        var myHeaders = new Headers();
        myHeaders.append("Accept", "application/json");
        myHeaders.append("Content-Type", "application/json");
        let body_register = JSON.stringify({
                              "email":this.state.email,
                              "firstname":this.state.firstname,
                              "lastname":this.state.lastname,
                              "password":this.state.password
                            })
        var register = {
                        method: 'POST',
                        headers: myHeaders,
                        body: body_register,
                       };

        console.log(body_register)
        if (annexe.checkInput1(this.state) == false) {
            Alert.alert(
              'Champs manquants',
              'Veuillez remplir tout les champs',
            );
        }
        else {
            fetch(annexe.ip+"users/create", register)
            .then(res => res.json())
            .then(res => {
                if(res.message == "Email déjà existant, veuillez en choisir un autre.") {
                    Alert.alert(
                        'Erreur',
                        'L\'E-mail est déjà utilisé.',
                    );
                } else {
                    if (res.error) {
                        Alert.alert(
                            'Erreur!',
                            'Une erreur est survenue',
                        );
                    } else {
                        Alert.alert(
                            'Félicitation !',
                            'Vous avez créer un compte.',
                        );
                        this.props.navigation.navigate('Login')
                    }
                }
            }).catch((error) => console.error("Erreur Register: " ,error));
         };
      };

  render() {
    return (
    // <ImageBackground source={require('../../assets/home.png')} style={{width: '100%', height: '100%'}}>
        <TouchableWithoutFeedback style={style.containerView} onPress={Keyboard.dismiss}>
          <ScrollView style={style.ScrollView}>
            <KeyboardAvoidingView behavior="padding">
                <View style={style.registerScreenContainer}>
                    <View style={style.registerFormView}>
                        <Image
                          style={{width: '100%', height: 360, marginBottom: -50}}
                          resizeMode="contain"
                          source={require('../../assets/StatFive.gif')}
                        />
                        <Text></Text>
                        <TextInput placeholder="Prénom" placeholderTextColor="#0090F8" style={style.registerFormTextInput} onChange={(e) => this.setState({firstname: e.nativeEvent.text})} />
                        <TextInput placeholder="Nom" placeholderTextColor="#0090F8" style={style.registerFormTextInput} onChange={(e) => this.setState({lastname: e.nativeEvent.text})} />
                        <TextInput placeholder="E-mail" placeholderTextColor="#0090F8" style={style.registerFormTextInput} onChange={(e) => this.setState({email: e.nativeEvent.text})} />
                        <TextInput placeholder="Mot de Passe" placeholderTextColor="#0090F8" style={style.registerFormTextInput} secureTextEntry={true} onChange={(e) => this.setState({password: e.nativeEvent.text})} />

                        <Button
                          buttonStyle={style.registerButton}
                          onPress={() => this.onRegisterPress()}
                          title="Créer votre compte"
                        />
                        <View style={style.MainContainer}>
                            <Text style={style.TextStyle} onPress={ ()=> this.props.navigation.navigate('Login') }>J'ai déjà un compte</Text>
                        </View>
                    </View>
                </View>
            </KeyboardAvoidingView>
          </ScrollView>
        </TouchableWithoutFeedback>
    // </ImageBackground>
    )
  }
}
