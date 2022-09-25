import { Flex, Box, Heading, List, Image } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { useEffect, useState } from 'react';
import withAuth from '../components/withAuth';
import { getAverageGoal } from "@mokhta_s/react-statfive-api"
import Leaderboard from '../components/Leaderboard';

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
                    <Flex justifyContent="center" w="75%">
                        <List spacing={3} textAlign="center" w="100%">
                            <Leaderboard data={teamRank} />
                        </List>
                    </Flex>
            </Flex>
        </Box>
    </Box>
  )
}

export default withAuth(Classement)