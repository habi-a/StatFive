import React, { useState, useRef } from "react";
import style from "./index";
import {Keyboard,
        Text,
        View,
        RefreshControl,
        TouchableWithoutFeedback,
        KeyboardAvoidingView,
        Image,
        ImageBackground} from 'react-native';
import { useNavigation } from "@react-navigation/native";
import { useEffect } from "react/cjs/react.development";
import { statMatchById } from "@mokhta_s/react-statfive-api";
import Icon from 'react-native-vector-icons/FontAwesome';
import { Video, AVPlaybackStatus } from 'expo-av';



const StatisticScreen = ({ route }) => {
    const video = React.useRef(null);
    const [stats, setStats] = useState(null)
    const [teamOne, setTeamOne] = useState(null)
    const [teamTwo, setTeamTwo] = useState(null)
    const [loading, setLoading] = useState(false)
    const navigation = useNavigation()
    const idMatch  = route.params.idMatch

    useEffect(() => {
        getMatchStatistic()
    }, [])

    const getMatchStatistic = async () => { 
        const result = await statMatchById(idMatch)
        if(result && result.data.data) {
            setStats(result.data.data)
            setTeamOne(result.data.data.team_blue)
            setTeamTwo(result.data.data.team_red)
        }
    }

    return (
            <KeyboardAvoidingView style={style.containerView} behavior="padding">
                <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
                    <View style={style.HeaderGenerique}>
                    <Image
                      style={{width: '100%', height: 180, marginBottom: -80}}
                      resizeMode="contain"
                      source={require('../../../public/StatFiveV3.png')}
                    />                    
                        <Icon name="backward" size={28} style={style.backLogo} onPress={() => navigation.goBack()}></Icon>
                        <Text style={style.Score}>{teamTwo?.goals} : {teamTwo?.goals}</Text>
                        <View style={{flexDirection: 'row', justifyContent:'space-around', height: 50}}>
                            <Text style={style.EquipeName}>{teamTwo?.name}</Text>
                            <Text style={style.EquipeName}>{teamOne?.name}</Text>
                        </View>
                        <View style={style.stats}>
                            <View style={style.seperator}/>
                            <Text style={style.titre}> Possession </Text>
                            <View style={{flexDirection: 'row', justifyContent:'space-around', height: "10%"}}>
                                <Text style={style.EquipeLeft}>{teamTwo?.possesion} %</Text>
                                <Text style={style.scoreseperator}>-</Text>
                                <Text style={style.EquipeRight}>{teamOne?.possesion} %</Text>
                            </View>
                            <View style={style.seperator}/>
                            <Text style={style.titre}> Vidéo du match </Text>
                            <View style={{flexDirection: 'row', justifyContent:'space-around', height: "10%"}}>
                                <Video
                                    ref={video}
                                    style={style.video}
                                    source={{
                                    uri: stats?.path,
                                    }}
                                    useNativeControls
                                    resizeMode="contain"
                                    isLooping={false}
                                />
                            </View>

                        </View>
                    </View>
                </TouchableWithoutFeedback>
            </KeyboardAvoidingView>
    );
}

export default StatisticScreen;