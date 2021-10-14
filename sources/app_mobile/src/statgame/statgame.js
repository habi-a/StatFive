import React, { Component } from "react";
import { createStackNavigator } from 'react-navigation-stack';
import { createAppContainer } from 'react-navigation';
import {Keyboard,
        Text,
        View,
        RefreshControl,
        TouchableWithoutFeedback,
        KeyboardAvoidingView,
        Image,
        ImageBackground} from 'react-native';
import { ScrollView } from "react-native-gesture-handler";

import style from "./style";
import annexe from '../../api_link'

export default class StatGameScreen extends Component {

    static navigationOptions = {
        headerShown:false,
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
        const id = this.state.id_match.toString();
        fetch(annexe.ip+"match/stat_match_by_id/"+id)
        .then(res => res.json())
        .then(res => {
          if (res && res.data && res.data.stats)
          {
            res.data.stats.forEach(color => {
              if (color.color === "blue")
                {
                  this.setState({blue: color});
                  this.getTeams(color.team_id,color.color);
                }
              if (color.color === "red")
                {
                  this.setState({red: color});
                  this.getTeams(color.team_id,color.color);
                }
            })
          }
        }).catch((error) => console.error("Erreur StatMatch: " ,error));
    }

    getTeams = (id,color) => {
      console.log(id,color)
        fetch(annexe.ip+"team/"+id)
        .then(res => res.json())
        .then(res => {
          if (color === "blue")
            {
              const tmp = this.state.blue;
              Object.assign(tmp,{name:res.data.name});
              this.setState({blue:tmp});
            }
          if (color === "red")
            {
              const tmp = this.state.red;
              Object.assign(tmp,{name:res.data.name});
              this.setState({red:tmp});
            }
        })
        .catch((error) => console.error("Erreur getTeams: " ,error))
    }


    componentDidMount = () => {
        this.statMatch()
    }

    render() {
        return (
        //<ImageBackground blurRadius={0.4} source={require('../../assets/gazon.jpg')} style={{width: '100%', height: '100%', opacity: 0.95}}>
            <KeyboardAvoidingView style={style.containerView} behavior="padding">
            <ScrollView
                refreshControl={
                    <RefreshControl
                        refreshing={this.state.refreshing}
                        onRefresh={this._onRefresh.bind(this)}
            />} >
                <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
                    <View style={style.HeaderGenerique}>
                    <Image
                      style={{width: '100%', height: 180, marginBottom: -80}}
                      resizeMode="contain"
                      source={require('../../assets/StatFiveV3.png')}
                    />
                        <Text style={style.Score}>{this.state.red.goals} : {this.state.blue.goals}</Text>
                        <View style={{flexDirection: 'row', justifyContent:'space-around', height: 50}}>
                            <Text style={style.EquipeLeftTitle}>{this.state.red.name}</Text>
                            <Text style={style.EquipeRightTitle}>{this.state.blue.name}</Text>
                        </View>
                        <View style={style.stats}>
                            <Text style={style.titre}> Tirs </Text>
                            <View style={{flexDirection: 'row', justifyContent:'space-around', height: "10%"}}>
                                <Text style={style.EquipeLeft}>2</Text>
                                <Text style={style.scoreseperator}>-</Text>
                                <Text style={style.EquipeRight}>4</Text>
                            </View>
                            <View style={style.seperator}/>
                            <Text style={style.titre}> Tirs cadrés </Text>
                            <View style={{flexDirection: 'row', justifyContent:'space-around', height: "10%"}}>
                                <Text style={style.EquipeLeft}>4</Text>
                                <Text style={style.scoreseperator}>-</Text>
                                <Text style={style.EquipeRight}>7</Text>
                            </View>
                            <View style={style.seperator}/>
                            <Text style={style.titre}> Passes </Text>
                            <View style={{flexDirection: 'row', justifyContent:'space-around', height: "10%"}}>
                                <Text style={style.EquipeLeft}>40</Text>
                                <Text style={style.scoreseperator}>-</Text>
                                <Text style={style.EquipeRight}>23</Text>
                            </View>
                            <View style={style.seperator}/>
                            <Text style={style.titre}> Passes réussites </Text>
                            <View style={{flexDirection: 'row', justifyContent:'space-around', height: "10%"}}>
                                <Text style={style.EquipeLeft}>20</Text>
                                <Text style={style.scoreseperator}>-</Text>
                                <Text style={style.EquipeRight}>13</Text>
                            </View>
                            <View style={style.seperator}/>
                            <Text style={style.titre}> Possession </Text>
                            <View style={{flexDirection: 'row', justifyContent:'space-around', height: "10%"}}>
                                <Text style={style.EquipeLeft}>{this.state.red.possesion} %</Text>
                                <Text style={style.scoreseperator}>-</Text>
                                <Text style={style.EquipeRight}>{this.state.blue.possesion} %</Text>
                            </View>
                        </View>
                    </View>
                </TouchableWithoutFeedback>
                </ScrollView>
            </KeyboardAvoidingView>
        //</ImageBackground>
        );
    }
}
