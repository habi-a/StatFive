import {
  Flex,
  Box,
  Heading,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionIcon,
  AccordionPanel,
} from "@chakra-ui/react";
import SimpleSidebar from "../components/Menu";
import Card from "../components/Card";
import { useStore } from "./index";
import withAuth from "../components/withAuth";
import { useEffect, useState } from "react";
import { getMyTeam, getMe } from "@mokhta_s/react-statfive-api";
import Profile from "../components/Profile";

const Profil = () => {
  const [teamID, setTeamID] = useState(null);
  const [team, setTeam] = useState([]);
  const [user, setUser] = useState(null);

  const getUser = async () => {
    const result = await getMe();
    if (!result?.data.error) {
      setUser(result.data.data);
    }
  };

  const getTeam = async () => {
    let result = await getMyTeam(teamID);
    if (result.length > 0) {
      setTeam(result);
    }
  };

  useEffect(() => {
    getUser();
  }, []);

  useEffect(() => {
    getTeam();
  }, [teamID]);

  return (
    <Box>
      <SimpleSidebar />
      <Box
        pos="relative"
        left={{ sm: "100px", md: "240px" }}
        w={{ md: "calc(100% -  240px)" }}
      >
        <Heading textAlign="center">Mon profil</Heading>
        <Profile data={user} />
        <Flex flexDir="row" padding="40px" ml="40px">
          {team &&
            team.map((elm, i) => (
              <Accordion key={i} allowToggle mr="20px">
                <AccordionItem>
                  <h2>
                    <AccordionButton
                      _expanded={{ bg: "black", color: "white" }}
                    >
                      <Box flex="1" textAlign="left">
                        {`Equipe ${elm.team.name}`}
                      </Box>
                      <AccordionIcon />
                    </AccordionButton>
                  </h2>
                  <AccordionPanel>
                    {elm.user.map((el) => (
                      <Card key={i} info={el} cantDelete={true} />
                    ))}
                  </AccordionPanel>
                </AccordionItem>
              </Accordion>
            ))}
        </Flex>
      </Box>
    </Box>
  );
};

export default withAuth(Profil);
