import {
  Flex,
  Text,
  Box,
  Heading,
  CircularProgress,
  CircularProgressLabel,
  Select,
} from "@chakra-ui/react";
import SimpleSidebar from "../components/Menu";
import { useEffect, useState } from "react";
import withAuth from "../components/withAuth";
import { getAverageGoal, getMe } from "@mokhta_s/react-statfive-api";
import Leaderboard from "../components/Leaderboard";

const Accueil = () => {
  const [teamRank, setTeamRank] = useState(null);
  const [stats, setStats] = useState(null);
  const [complex, setComplex] = useState(null);
  const [info, setInfo] = useState(null);
  const [allComplex, setAllComplex] = useState(null);

  const getMyInfo = async () => {
    const result = await getMe();
    if (!result.data.error) {
      if (result.data.data.complexes) {
        setAllComplex(result.data.data.complexes);
      }
      setStats(result.data.data.stats);
      setComplex(result.data.data.complex);
      setInfo(result.data.data);
    }
  };

  const getGoalRank = async () => {
    const result = await getAverageGoal();
    if (result.length > 0) setTeamRank(result);
    else setTeamRank([]);
  };

  useEffect(() => {
    getGoalRank();
    getMyInfo();
  }, []);

  return (
    <Box>
      <SimpleSidebar />
      <Box
        pos="relative"
        left={{ sm: "100px", md: "240px" }}
        w={{ md: "calc(100% -  240px)" }}
      >
        <Heading textAlign="center">Accueil</Heading>
        <Flex flexDir="row" justifyContent="space-around">
          <Box>
            <Heading size="md" mb="15px" mt="15px">
              Classement général
            </Heading>
            <Box w="100%">
              <Leaderboard data={teamRank} />
            </Box>
          </Box>
        </Flex>
        <Box borderTop="5px solid white" mt="25px">
          {info?.role >= 1 ? (
            <Heading size="md" mt="25px" textAlign="center">
              Statistiques sur le complexe : {complex?.name}
            </Heading>
          ) : (
            <Heading size="md" mt="25px" textAlign="center">
              Statistiques des équipes de : {info?.lastname} {info?.firstname}
            </Heading>
          )}
          {info?.role === 2 && (
            <Select
              w="25%"
              m="25px auto"
              placeholder="Choisir un complexe"
              onChange={(e) => {
                if (e.target.value) {
                  setComplex(JSON.parse(e.target.value));
                  setStats(JSON.parse(e.target.value).stats);
                }
              }}
            >
              {allComplex &&
                allComplex.length > 0 &&
                allComplex.map((el, i) => (
                  <option key={i} value={`${JSON.stringify(el)}`}>
                    {el.name}
                  </option>
                ))}
            </Select>
          )}
          <Flex justifyContent="space-evenly" mt="30px">
            <CircularProgress size="200px" value={100} color="#1C3879">
              <CircularProgressLabel>
                <Text fontSize="25px">
                  {stats?.nb_but} {stats ? "but" : ""}
                  {stats?.nb_but > 0 ? "s" : ""}
                </Text>
              </CircularProgressLabel>
            </CircularProgress>
            <CircularProgress size="200px" value={100} color="#1C3879">
              <CircularProgressLabel>
                <Text fontSize="25px">
                  {stats?.nb_match} {stats ? "match" : ""}
                  {stats?.nb_match > 0 ? "s" : ""}
                </Text>
              </CircularProgressLabel>
            </CircularProgress>
          </Flex>
        </Box>
      </Box>
    </Box>
  );
};

export default withAuth(Accueil);
