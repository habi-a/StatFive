import { Flex, Box, Heading, List, ListItem, ListIcon } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { GiTrophyCup, GiMedal } from "react-icons/gi"
import { useEffect, useState } from 'react';
import withAuth from '../components/withAuth';
import { getAverageGoal } from "@mokhta_s/react-statfive-api"

const Classement = () => {
    const [teamRank, setTeamRank] = useState(null);

    const getGoal = async () => {
        let result = await getAverageGoal()
        if(!result.error)
            setTeamRank(result)
    }

    useEffect(() => {
        getGoal()
    }, [])

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left={{sm: "100px", md: "240px"}} w={{ md:"calc(100% -  240px)"}}>
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