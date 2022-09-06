import { Flex, Text, Box, Heading, Button, AspectRatio, useToast } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { useEffect, useState } from 'react';
import router from 'next/router'
import {useStore} from "./index"
import axios from "axios"
import { API_URL } from "../static";
import Select from 'react-select'
import withAuth from '../components/withAuth';
import { getAllTeam, addVideo } from "@mokhta_s/react-statfive-api"

const Admin = () => {
    const dataUser = useStore(state => state.data)
    const [allTeam, setAllTeam] = useState([]);
    const [mp4, setMp4] = useState(null);
    const [teamOne, setTeamOne] = useState(null);
    const [teamTwo, setTeamTwo] = useState(null);

    const token = useStore(state => state.token)
    const toast = useToast()

    const getTeam = async () => {
      let result = await getAllTeam(API_URL)
      if(!result.error)
        setAllTeam(result)
    }


      useEffect(() => {
        if(false) // data && dataUser.role !== 1
          return router.replace('/accueil')
        getTeam()
      }, [dataUser])
    
      const addNewVideo = async () => {
        const result = await addVideo(mp4, teamOne, teamTwo)
        if(!result?.data?.error) {
            toast({
                title: "L'analyse vidéo a bien été lancé",
                description: "Elle sera bientôt disponible..",
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
                    <Heading textAlign="center" mb="25px">Création du match</Heading>
                    <Flex w="100%" justifyContent="center" flexDir="column">
                        <Text as="h1" fontSize="30px" textAlign="center">Equipe 1</Text>
                        <Flex justifyContent="center">
                            <Select options={allTeam} placeholder="Choisissez une équipe" onChange={(e) => setTeamOne(e.value)}/>
                        </Flex>
                        <Text as="h6" fontSize="30px" textAlign="center" >Equipe 2</Text>
                        <Flex justifyContent="center">
                            <Select options={allTeam} placeholder="Choisissez une équipe" onChange={(e) => setTeamTwo(e.value)}/>
                        </Flex>
                        
                    </Flex>
                    <Flex justifyContent="center" alignItems="center" flexDirection="column" mt="25px">
                        <input type="file" name="video" id="video" className="choicevideo" accept=".mp4" onChange={(e) => setMp4(e.target.files[0])}/>
                        <AspectRatio maxW="560px" w="560px" h="250" ratio={1} mt="25px">
                        <iframe
                          title="naruto"
                          src={mp4 && URL.createObjectURL(mp4)}
                          allowFullScreen
                        />
                      </AspectRatio>
                    {mp4 && teamOne && teamTwo && <Button mt="25px" onClick={() => addNewVideo()}>Valider la création</Button>}
                    </Flex>
        </Box>
    </Box>
  )
}

export default withAuth(Admin)