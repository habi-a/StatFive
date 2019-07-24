import React, { Component } from "react";
import styles from './style'
import annexe from '../../annexe'
import {List,
        ListItem} from 'native-base';

import {Keyboard, 
        Text, 
        View, 
        TouchableWithoutFeedback, 
        KeyboardAvoidingView,
        RefreshControl,
        TouchableOpacity,
        AsyncStorage,
        ScrollView,
        ImageBackground,
        Alert } from 'react-native';

export default class AccueilScreen extends Component {

    static navigationOptions = {
      header:null,
    };

    constructor(props){
        super(props)
        this.state={
            data_prive: ["Bad", "Basket","Tennis"],
            data_public: ["Piscine", "Vélo"],
            user: {name: ''},
            refreshing: false,
        }
    }

    _onRefresh = () => {
        this.setState({refreshing: true});
        this.fetchData().then(() => {
            this.setState({refreshing: false});
          });
    }

    fetchData = async() => {
        this.getPublicGame()
    }

    getPublicGame() {
        const header = {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                Authorization: 'Bearer '+ this.state.user.token
            },
        };
        fetch(annexe.ip+"ATTENTEAPIICI", header)
        .then(res => res.json())
        .then(res => {console.log(res.public_games)
        this.setState({data_public: res.public_games})
    })
        .catch(error => console.error("Erreur PublicGame: ", error))
    }

    _recupUser = async () => {
        try {
            const value = await AsyncStorage.getItem('user');
            if (value !== null) {
                this.setState({user: JSON.parse(value)})
                console.log("User: ",this.state.user.token);

            }
        } catch (error) {
            console.error("Erreur User: ",error)
        }
    };

    onLogout() {
        Alert.alert(
            'Attention',
            'Voulez-vous vraiment quitter l\'application ?',
            [
              {text: 'Oui, je le souhaite', onPress: () => this.clearAsyncStorage()},
              {
                text: 'Non',
                onPress: () => console.log('Cancel Pressed'),
                style: 'cancel',
              },
            ],
            {cancelable: false},
          );
    }
    
    clearAsyncStorage = async() => {
        AsyncStorage.clear();
        this.props.navigation.navigate("Login");
    }

    componentDidMount = async () => {
        const user = await this._recupUser()
        this.getPublicGame()
    }

  render() {
    return (
    <ImageBackground blurRadius={2} source={require('../../assets/background-home.png')} style={{width: '100%', height: '100%', opacity: 0.95}}>
        <KeyboardAvoidingView style={styles.containerView} behavior="padding">
            <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
                <View style={styles.HeaderGenerique}>
                    <Text style={styles.logoText}>
                        <Text style={{color:'white'}}>Match - </Text>
                        <Text style={{color:'white', fontSize: 24}} onPress={() => this.onLogout()} >Fr4nck</Text>                    
                    </Text>
                </View>
            </TouchableWithoutFeedback>
            <View>
                <ScrollView
                        refreshControl={
                            <RefreshControl
                                refreshing={this.state.refreshing}
                                onRefresh={this._onRefresh.bind(this)}
                            />} >
                    <List>
                        <ListItem>
                            <Text style={styles.FirstLetter}>Historique de Matchs</Text>
                        </ListItem>
                        {  this.state.data_public.map(data => ( <ListItem >
                            <TouchableOpacity onPress={() =>  this.props.navigation.navigate('StatGame', {id: data.id})} title="0">
                                <Text  style={styles.listItems}>{data.title} # C'est un léger test pour voir la transparence {data.id}</Text>
                            </TouchableOpacity>
                        </ListItem>
                        ) ) }
                    </List>
                </ScrollView>
            </View>
        </KeyboardAvoidingView>
    </ImageBackground>
    );
  }
}
