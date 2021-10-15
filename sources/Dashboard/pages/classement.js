import { Flex, Box, Heading, List, ListItem, ListIcon } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { GiTrophyCup, GiMedal } from "react-icons/gi"
import { useEffect, useState } from 'react';
import axios from "axios"
import { API_URL } from "../static";
import withAuth from '../components/withAuth';

const Classement = () => {
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
            <Heading textAlign="center" mb="50px">Classement moyenne de but</Heading>
            <Flex flexDir="row" justifyContent="space-around">
                    <Flex justifyContent="center" w="100%">
                        <List spacing={3} textAlign="center" w="100%">
                            {teamRank && teamRank.map((el, i) => 
                                i <= 2
                                ? <ListItem bgColor="#84C9D5" cursor="pointer"> <ListIcon as={i == 0 ? GiTrophyCup : GiMedal} color={i == 0 ? "gold" : i == 1 ? "silver" : "bronze"} />{el.name}</ListItem> 
                                : <ListItem bgColor="#F3FAFB" cursor="pointer" mb="10px">{el.name}</ListItem> 
                            )}
                        </List>
                    </Flex>
            </Flex>
        </Box>
    </Box>
  )
}

export default withAuth(Classement)