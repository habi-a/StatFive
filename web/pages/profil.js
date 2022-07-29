import { Flex, Box, Heading, Accordion, AccordionItem, AccordionButton, AccordionIcon, AccordionPanel } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import Card from "../components/Card"
import {useStore} from "./index"
import withAuth from '../components/withAuth'
import { useEffect, useState } from 'react'
import axios from 'axios'
import { API_URL } from "../static";
import { getAllTeam, getMyTeam } from '@mokhta_s/react-statfive-api'

const Profil = () => {
  const [teamID, setTeamID] = useState(null)
  const [team, setTeam] = useState([])

  const userID = useStore((state) => state.data.id)

  const allTeam = async () => {
    let result = await getAllTeam(API_URL)
    if(result?.length > 0) {
      setTeamID(result)
    }
  }

  const getTeam = async () => {
    console.log(teamID, userID)
    let result = await getMyTeam(API_URL, teamID, userID)
    console.log(result)
    result && result.map(async (elm) => {
          await axios.get(elm).then(res => {
              const arrayTeam = res.data.data.user
              console.log(arrayTeam)
              if(arrayTeam.length === 5) {
                if(arrayTeam.find(o => o.id === userID)) {
                  setTeam([arrayTeam])
                }
              }
            })  
          .catch(err => {
            return err.response
          })
        })
  }

  useEffect(() => {
    allTeam()
  }, [])

  useEffect(() => {
    if(teamID?.length > 0)
      getTeam()
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
                                {`Equipe ${++i}`}
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