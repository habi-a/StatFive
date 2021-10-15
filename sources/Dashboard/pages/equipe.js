import { Flex, Box, Heading, Button, Input } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import CardEmpty from '../components/CardEmpty'
import axios from "axios"
import { useEffect, useState } from 'react';
import {useStore} from "./index"
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { API_URL } from "../static";
import withAuth from '../components/withAuth'
import router from 'next/router'

const Equipe = () => {
    const [teamName, setTeamName] = useState('')
    const resetTeam = useStore(state => state.resetTeam)
    const arrayTeam = useStore(state => state.teamUser)
    const dataUser = useStore((state) => state.data)

    useEffect(() => {
      if(dataUser && dataUser.role !== 1)
        return router.replace('/accueil')
      resetTeam()
    }, [dataUser])

    const createTeam = async () => {
        await axios.post(
            [API_URL] + `/team/create_team`,
            [{name: teamName, player: arrayTeam }])
          .then(res => {
              toast.success("L'équipe a été créée avec succès", {
                  position: "bottom-right",
                  autoClose: 5000,
                  hideProgressBar: false,
                  closeOnClick: true,
                  pauseOnHover: true,
                  draggable: true,
                  progress: undefined,
                  });
          })
          .catch(err => console.log('Erreur', err)
          );
    }

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left="240px" w="calc(100% -  240px)">
            <Heading textAlign="center">Création d'équipe</Heading>
            <Input type="text" value={teamName} placeholder="Nom de l'équipe" mt="25px" w="50%" errorBorderColor="red.300" isInvalid={teamName.length < 1} ml="40px" onChange={(e) => setTeamName(e.target.value)}/>
            <Flex flexDir="row" justifyContent="space-between" padding="40px">
                <CardEmpty />
                <CardEmpty />
                <CardEmpty />
                <CardEmpty />
                <CardEmpty />
            </Flex>
            {arrayTeam.length === 5 && teamName.length > 0 && <Button ml="40px" onClick={() => createTeam()} colorScheme="blue">Valider l'équipe</Button>}
            <ToastContainer
                            position="bottom-right"
                            autoClose={5000}
                            hideProgressBar={false}
                            newestOnTop={false}
                            closeOnClick
                            rtl={false}
                            pauseOnFocusLoss
                            draggable
                            pauseOnHover
                        />
        </Box>
    </Box>
  )
}

export default withAuth(Equipe)