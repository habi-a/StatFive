import { Flex, Text, Box, Heading, List, ListItem, ListIcon, Link } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { Line, Doughnut } from 'react-chartjs-2';
import { data, options, dataPass, dataVictory } from '../static/data';
import { GiTrophyCup, GiMedal } from "react-icons/gi"
import { useEffect, useState } from 'react';
import axios from "axios"
import { API_URL } from "../static";
import withAuth from '../components/withAuth';

const Accueil = () => {
    const [teamRank, setTeamRank] = useState(null);

    const getAverageGoal = async () => {
        await axios.get(
            API_URL + `/team/average_team`).then(res => {
                res.data.data.sort((a, b) => b.moyenne_goal - a.moyenne_goal);
                setTeamRank(res.data.data)
            })
          .catch(err => {
            console.log(err)
          });
    }

    useEffect(() => {
        getAverageGoal()
    }, [])

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left="240px" w="calc(100% -  240px)">
            <Heading textAlign="center">Accueil</Heading>
            <Flex w="700px" h="auto" mb="75px" ml="125px">
                <Line data={data} options={options} />
                <Line data={dataPass} options={options} />
            </Flex>
            <Flex flexDir="row" justifyContent="space-around">
                <Box ml="125px">
                    <Heading mb="25px" >Classement général</Heading>
                    <Flex justifyContent="center" w="100%">
                        <List spacing={3} textAlign="center" w="100%">
                            {teamRank && teamRank.map((el, i) => 
                                i <= 4 ? i <= 2
                                ? <ListItem bgColor="#84C9D5" cursor="pointer"> <ListIcon as={i == 0 ? GiTrophyCup : GiMedal} color={i == 0 ? "gold" : i == 1 ? "silver" : "bronze"} />{el.name}</ListItem> 
                                : <ListItem bgColor="#F3FAFB" cursor="pointer" mb="10px">{el.name}</ListItem> 
                                : null
                            )}
                            <Link href="/classement" color="blueteal.500">
                                <Text>Voir plus..</Text>
                            </Link>
                        </List>
                    </Flex>
                </Box>
                <Box  w="300px" h="300px">
                    <Doughnut data={dataVictory} />
                </Box>
            </Flex>
        </Box>
    </Box>
                            
  )
}

export default withAuth(Accueil)