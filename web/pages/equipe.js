import { Flex, Box, Heading, Button, Input, useToast } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import CardEmpty from '../components/CardEmpty'
import axios from "axios"
import { useEffect, useState } from 'react';
import {useStore} from "./index"
import withAuth from '../components/withAuth'
import router from 'next/router'
import { createTeam } from '@mokhta_s/react-statfive-api';

const Equipe = () => {
    const toast = useToast()
    const [teamName, setTeamName] = useState('')
    const resetTeam = useStore(state => state.resetTeam)
    const arrayTeam = useStore(state => state.teamUser)
    const dataUser = useStore((state) => state.data)


    useEffect(() => {
      if(false) // dataUser && dataUser.role !== 1
        return router.replace('/accueil')
      resetTeam()
    }, [dataUser])

    const createNewTeam = async () => {
        const result = await createTeam(teamName, arrayTeam)
        if(!result?.data.error) {
            toast({
                title: "La création de l'équipe a été effectué",
                description: "Votre équipe est disponible",
                status: 'success',
                duration: 5000,
                isClosable: true,
              })
        }
    }

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left={{sm: "100px", md: "240px"}} w={{ md:"calc(100% -  240px)"}}>
            <Heading textAlign="center">Création d'équipe</Heading>
            <Input type="text" value={teamName} placeholder="Nom de l'équipe" mt="25px" w="50%" errorBorderColor="red.300" isInvalid={teamName.length < 1} ml="40px" onChange={(e) => setTeamName(e.target.value)}/>
            <Flex flexDir={{base: "column", md: "row"}} justifyContent="space-between" padding="40px">
                <CardEmpty />
                <CardEmpty />
                <CardEmpty />
                <CardEmpty />
                <CardEmpty />
            </Flex>
            {arrayTeam.length === 5 && teamName.length > 0 && <Button ml="40px" onClick={() => createNewTeam()} colorScheme="blue">Valider l'équipe</Button>}
            {/* <ToastContainer
                            position="bottom-right"
                            autoClose={5000}
                            hideProgressBar={false}
                            newestOnTop={false}
                            closeOnClick
                            rtl={false}
                            pauseOnFocusLoss
                            draggable
                            pauseOnHover
                        /> */}
        </Box>
    </Box>
  )
}

export default withAuth(Equipe)