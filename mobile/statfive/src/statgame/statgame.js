import React, { Component } from "react";
import styles from './style'
import annexe from '../../annexe'

import {Keyboard, 
    Text, 
    View, 
    TouchableWithoutFeedback, 
    KeyboardAvoidingView,
    RefreshControl,
    ScrollView,
    ImageBackground} from 'react-native';

export default class StatGameScreen extends Component {

    static navigationOptions = {
        header:null,
      };
  
      constructor(props){
            super(props)
            this.state={
                refreshing: false,
                id_match: this.props.navigation.state.params.id,
                stats: [],
                blue: {},
                red: {}
        }
    }

    _onRefresh = () => {
        this.setState({refreshing: true});
        this.fetchData().then(() => {
            this.setState({refreshing: false});
          });
    }

    statMatch = () => {
        fetch(annexe.ip+"match/"+this.state.id_match)
        .then(res => res.json())
        .then(res => {
            this.setState({blue: res[0].blue})
            this.setState({red: res[0].red})
        }).catch((error) => console.error("Erreur StatMatch: " ,error));
    }

    componentDidMount = () => {
        this.statMatch()
    }

    render() {
        return (
        <ImageBackground blurRadius={0.4} source={require('../../assets/gazon.jpg')} style={{width: '100%', height: '100%', opacity: 0.95}}>
            <KeyboardAvoidingView style={styles.containerView} behavior="padding">
                <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
                    <View style={styles.HeaderGenerique}>
                        <Text style={styles.Score}> {this.state.red.goals} : {this.state.blue.goals} </Text>
                        <View style={{flexDirection: 'row', justifyContent:'space-around', height: 50}}>
                            <Text style={styles.EquipeLeft}>{this.state.red.team_name}</Text>
                            <Text style={styles.EquipeRight}>{this.state.blue.team_name}</Text>
                        </View>
                            <ImageBackground source={require('../../assets/logo.png')} style={{width: '100%', height: '120%',marginTop:20 , opacity: 0.80}}></ImageBackground>
                            <View style={styles.stats}>
                            <Text style={styles.titre}> Tirs </Text>
                            <View style={{flexDirection: 'row', justifyContent:'space-around', height: 50}}>
                                <Text style={styles.EquipeLeft}>2</Text>
                                <Text style={styles.EquipeRight}>4</Text>
                            </View>
                            <Text style={styles.titre}> Tirs cadrés </Text>
                            <View style={{flexDirection: 'row', justifyContent:'space-around', height: 50}}>
                                <Text style={styles.EquipeLeft}>2</Text>
                                <Text style={styles.EquipeRight}>7</Text>
                            </View>
                            <Text style={styles.titre}> Passes </Text>
                            <View style={{flexDirection: 'row', justifyContent:'space-around', height: 50}}>
                                <Text style={styles.EquipeLeft}>40</Text>
                                <Text style={styles.EquipeRight}>23</Text>
                            </View>
                            <Text style={styles.titre}> Passes réussites </Text>
                            <View style={{flexDirection: 'row', justifyContent:'space-around', height: 50}}>
                                <Text style={styles.EquipeLeft}>20</Text>
                                <Text style={styles.EquipeRight}>13</Text>
                            </View>
                            <Text style={styles.titre}> Possession </Text>
                            <View style={{flexDirection: 'row', justifyContent:'space-around', height: 50}}>
                                <Text style={styles.EquipeLeft}>{this.state.red.possesion} %</Text>
                                <Text style={styles.EquipeRight}>{this.state.blue.possesion} %</Text>
                            </View>
                        </View>
                    </View>
                </TouchableWithoutFeedback>
                <View>
                    <ScrollView
                        refreshControl={
                            <RefreshControl
                                refreshing={this.state.refreshing}
                                onRefresh={this._onRefresh.bind(this)}
                    />} >
                    </ScrollView>
                </View>
            </KeyboardAvoidingView>
        </ImageBackground>
        );
    }
}