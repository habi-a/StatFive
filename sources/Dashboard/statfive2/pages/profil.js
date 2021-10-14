import { Flex, Box, Heading, Accordion, AccordionItem, AccordionButton, AccordionIcon, AccordionPanel } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import Card from "../components/Card"
import {useStore} from "./index"
import withAuth from '../components/withAuth'
import { useEffect, useState } from 'react'
import axios from 'axios'
import { API_URL } from "../static";

const Profil = () => {
  const [teamID, setTeamID] = useState(null)
  const [team, setTeam] = useState([])

  const userID = useStore((state) => state.data.id)

  const allTeam = async () => {
    await axios.get(
    API_URL + `/team/all_team`).then(res => {
        setTeamID(res.data.data);
    })  
  .catch(err => {
    console.log(err)
  });
}

  const getMyTeam = () => {
    teamID && teamID.map(async (elm) => {
      await axios.get(
        API_URL + `/team/${elm.id}`).then(res => {
          const arrayTeam = res.data.data.user
          if(arrayTeam.length === 5) {
            if(arrayTeam.find(o => o.id === userID)) {
              setTeam((array) => [...array, arrayTeam])
            }
          }
        })  
      .catch(err => {
        console.log(err)
      });
    })
  }

  useEffect(() => {
    allTeam()
  }, [])

  useEffect(() => {
    getMyTeam()
  }, [teamID])

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left="240px" w="calc(100% -  240px)">
            <Heading textAlign="center">Mon profil</Heading>
            <Flex flexDir="row" padding="40px" ml="40px">
              {team && team.map((elm, i) => 
                <Accordion allowToggle mr="20px">
                  <AccordionItem>
                        <h2>
                            <AccordionButton _expanded={{ bg: "black", color: "white" }}>
                              <Box flex="1" textAlign="left">
                                {`Equipe ${i}`}
                              </Box>
                            <AccordionIcon />
                          </AccordionButton>
                        </h2>
                      <AccordionPanel> 
                        {elm.map((el) => 
                        <Card info={el} cantDelete={true} />
                        )}
                      </AccordionPanel>
                  </AccordionItem>
                </Accordion>
              )}
            </Flex>
        </Box>
    </Box>
  )
}

export default withAuth(Profil)