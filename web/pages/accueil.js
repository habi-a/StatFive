import { Flex, Text, Box, Heading, List, ListItem, Link } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { useEffect, useState } from 'react';
import { API_URL } from "../static";
import withAuth from '../components/withAuth';
import { getAverageGoal } from '@mokhta_s/react-statfive-api'
import {useStore} from "./index"

const Accueil = () => {
    const [teamRank, setTeamRank] = useState(null);
    const token = useStore(state => state.token)

    const getGoalRank = async () => {
        const result = await getAverageGoal()
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
        <Box pos="relative" left={{sm: "100px", md: "240px"}} w={{ md:"calc(100% -  240px)"}}>
            <Heading textAlign="center" >Accueil</Heading>
            <Flex flexDir="row" justifyContent="space-around">
                <Box>
                    <Heading mb="25px" >Classement général</Heading>
                    <Flex justifyContent="center" w="100%">
                        <List spacing={3} textAlign="center" w="100%">
                            {teamRank && teamRank.map((el, i) => 
                                i <= 4 ? i <= 2
                                ? <ListItem key={i} bgColor="#84C9D5" cursor="pointer">{el.name}</ListItem> 
                                : <ListItem key={i} bgColor="#F3FAFB" cursor="pointer" mb="10px">{el.name}</ListItem> 
                                : null
                            )}
                            <Link href="/classement" color="blueteal.500">
                                <Text>Voir plus..</Text>
                            </Link>
                        </List>
                    </Flex>
                </Box>
            </Flex>
        </Box>
    </Box>
                            
  )
}

export default withAuth(Accueil)