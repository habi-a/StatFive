import React, { useEffect, useState } from "react";
import style from "./index";
import {
        Keyboard,
        View,
        Text,
        List,
        ListItem,
        ScrollView,
        TouchableOpacity,
        FlatList,
        TouchableWithoutFeedback,
        RefreshControl
    } from 'react-native';
import { matchListHistoric } from "@mokhta_s/react-statfive-api";
import Icon from 'react-native-vector-icons/FontAwesome';

import { useNavigation } from "@react-navigation/native";




const AccueilScreen = () => {
    const [match, setMatch] = useState([])
    const [refreshing, setRefreshing] = useState(false)

    const navigation = useNavigation()

    useEffect(() => {
        allMatch()
    }, [])

    const allMatch = async () => {
        setRefreshing(true)
        const result = await matchListHistoric()
        console.log('la', result)
        if(result && result.length > 0) {
            setMatch(result)
        }
        setRefreshing(false)
    }

    return (
        <View style={style.containerView}>
            <TouchableWithoutFeedback onPress={() => Keyboard.dismiss()}>
                <View style={style.header}>
                    <Text style={style.logoText}>
                        <Text style={{color:'white'}}>Accueil</Text>
                    </Text>
                    <Icon style={style.icon_trophy} name="trophy" size={36} onPress={() => navigation.navigate('Classement')}></Icon>
                    <Icon style={style.icon_profil} name="user" size={36} onPress={() => navigation.navigate('Profil')}></Icon>
                </View>
            </TouchableWithoutFeedback>
            <Text style={style.FirstLetter}>Historique de Matchs</Text>
                <FlatList data={match} refreshing={refreshing} onRefresh={() => allMatch()} renderItem={(elem) => {
                    return <TouchableOpacity key={elem.item.id} onPress={() =>  navigation.navigate('Statistic', { idMatch: elem.item.id})} title="0">
                        <View style={{ width: "96%", height: 50, flex:1, alignItems: "left", justifyContent: "center", margin: "2%", backgroundColor: "#fff", borderRadius: 5, borderWidth: 2, borderStyle: "solid", borderColor: "#0090F8" }}>
                            <Text  style={style.listItems}> Match n°{elem.item.id} | {elem.item.name} </Text>
                        </View>
                    </TouchableOpacity>
                }} />
        </View>
    );
}

export default AccueilScreen;