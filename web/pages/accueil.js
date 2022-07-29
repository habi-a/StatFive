import { Flex, Text, Box, Heading, List, ListItem, ListIcon, Link } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { Line, Doughnut } from 'react-chartjs-2';
import { data, options, dataPass, dataVictory } from '../static/data';
import { GiTrophyCup, GiMedal } from "react-icons/gi"
import { useEffect, useState } from 'react';
import { API_URL } from "../static";
import withAuth from '../components/withAuth';
import { getAverageGoal } from '@mokhta_s/react-statfive-api'

const Accueil = () => {
    const [teamRank, setTeamRank] = useState(null);

    const getGoalRank = async () => {
        let result = await getAverageGoal(API_URL)
        if(result.length > 0)
            setTeamRank(result)
        else
            setTeamRank([])
    }

    useEffect(() => {
        getGoalRank()
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
                                ? <ListItem key={i} bgColor="#84C9D5" cursor="pointer"> <ListIcon as={i == 0 ? GiTrophyCup : GiMedal} color={i == 0 ? "gold" : i == 1 ? "silver" : "bronze"} />{el.name}</ListItem> 
                                : <ListItem key={i} bgColor="#F3FAFB" cursor="pointer" mb="10px">{el.name}</ListItem> 
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