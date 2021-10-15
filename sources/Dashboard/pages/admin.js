import { Flex, Text, Box, Heading, Button, AspectRatio } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { data } from '../static/data';
import { useEffect, useState } from 'react';
import router from 'next/router'
import {useStore} from "./index"
import axios from "axios"
import { API_URL } from "../static";
import Select from 'react-select'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import withAuth from '../components/withAuth';

const Admin = () => {
    const dataUser = useStore(state => state.data)
    const [allTeam, setAllTeam] = useState([]);
    const [mp4, setMp4] = useState(null);
    const [teamOne, setTeamOne] = useState(null);
    const [teamTwo, setTeamTwo] = useState(null);

    const token = useStore(state => state.token)


    const getAllTeam = async () => {
        await axios.get(
            API_URL + `/team/all_team`).then(res => {
                let arrayObj = res.data.data
                setAllTeam(res.data.data);
                arrayObj = arrayObj.map(item => {
                    return {
                      value: item.id,
                      label: item.name
                    };
                  });
                setAllTeam(arrayObj)
            })
          .catch(err => {
            console.log(err)
          });
      }

      useEffect(() => {
        if(data && dataUser.role !== 1)
          return router.replace('/accueil')
        getAllTeam()
      }, [data])
    
      const addVideo = async () => {
        var bodyFormData = new FormData();
        bodyFormData.append('video', mp4);
        bodyFormData.append('team_one', teamOne);
        bodyFormData.append('team_two', teamTwo);
    
    
        var headers = {
          'Content-Type': 'multipart/form-data',
          "Access-Control-Allow-Origin": "*",
          'api-token': token
        }
        await axios.post(
            [API_URL] + `/match`,
            bodyFormData, { headers: headers })
          .then(res => {
              toast.success("L'analyse vidéo a bien été lancé", {
                  position: "bottom-right",
                  autoClose: 5000,
                  hideProgressBar: false,
                  closeOnClick: true,
                  pauseOnHover: true,
                  draggable: true,
                  progress: undefined,
                  });
              console.log('Analyse vidéo en cours')
          })
          .catch(err => console.log('Erreur', err)
          );
      }
    

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left="240px" w="calc(100% -  240px)">
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
                    {mp4 && teamOne && teamTwo && <Button mt="25px" onClick={() => addVideo()}>Valider la création</Button>}
                    </Flex>
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

export default withAuth(Admin)