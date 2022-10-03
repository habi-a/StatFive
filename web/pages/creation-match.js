import {
  Flex,
  Text,
  Box,
  Heading,
  Button,
  Input,
  useToast,
  AspectRatio,
} from "@chakra-ui/react";
import SimpleSidebar from "../components/Menu";
import { useEffect, useState, useCallback } from "react";
import router from "next/router";
import { useStore } from "./index";
import axios from "axios";
import { API_URL } from "../static";
import Select from "react-select";
import withAuth from "../components/withAuth";
import { getAllTeam, addVideo } from "@mokhta_s/react-statfive-api";
import { useDropzone } from "react-dropzone";

const Admin = () => {
  const dataUser = useStore((state) => state.data);
  const [allTeam, setAllTeam] = useState([]);
  const [mp4, setMp4] = useState(null);
  const [teamOne, setTeamOne] = useState(null);
  const [teamTwo, setTeamTwo] = useState(null);
  const toast = useToast();

  const getTeam = async () => {
    let result = await getAllTeam(API_URL);
    if (!result.error) setAllTeam(result);
  };

  useEffect(() => {
    getTeam();
  }, [dataUser]);

  const addNewVideo = async () => {
    const result = await addVideo(mp4, teamOne, teamTwo);
    if (!result?.data?.error) {
      toast({
        title: "L'analyse vidéo a bien été lancé",
        description: "Elle sera bientôt disponible..",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const onDrop = useCallback((acceptedFiles) => {
    setMp4(acceptedFiles[0]);
  }, []);

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <Box>
      <SimpleSidebar />
      <Box
        pos="relative"
        left={{ sm: "100px", md: "240px" }}
        w={{ md: "calc(100% -  240px)" }}
      >
        <Heading textAlign="center" mb="25px">
          Création du match
        </Heading>
        <Flex w="100%" justifyContent="space-evenly" flexDir="row" mb="50px">
          <Flex justifyContent="center" flexDir="column">
            <Text as="h1" mb="15px" fontSize="30px" textAlign="center">
              Equipe 1
            </Text>
            <Select
              datatestid="match_team"
              options={allTeam}
              placeholder="Choisissez une équipe"
              onChange={(e) => setTeamOne(e.value)}
            />
          </Flex>

          <Flex justifyContent="center" flexDir="column">
            <Text as="h6" mb="15px" fontSize="30px" textAlign="center">
              Equipe 2
            </Text>
            <Select
              datatestid="match_team"
              options={allTeam}
              placeholder="Choisissez une équipe"
              onChange={(e) => setTeamTwo(e.value)}
            />
          </Flex>
        </Flex>
        <Flex
          justifyContent="center"
          alignItems="center"
          flexDirection="column"
          mt="25px"
        >
          {mp4 === null && (
            <Box
              cursor="pointer"
              p="50px"
              backgroundColor="#DFD3C3"
              border="3px dashed #1C3879"
              borderRadius="5px"
              {...getRootProps()}
            >
              <Input datatestid="match_video" {...getInputProps()} />
              <Text fontWeight="bold">
                Déposer votre fichier ici, ou cliquez pour sélectionner un
                fichier
              </Text>
            </Box>
          )}
          {mp4 && (
            <AspectRatio maxW="560px" w="560px" h="250" ratio={1} mt="25px">
              <iframe
                title="naruto"
                src={mp4 && URL.createObjectURL(mp4)}
                allowFullScreen
              />
            </AspectRatio>
          )}
          <Flex>
            {mp4 && (
              <Button
                mt="25px"
                mr="15px"
                datatestid="match_change_video"
                background="red.600"
                color="white"
                onClick={() => setMp4(null)}
              >
                Changer de vidéo
              </Button>
            )}
            {mp4 && teamOne && teamTwo && (
              <Button
                datatestid="match_creation"
                mt="25px"
                backgroundColor="green.600"
                color="white"
                onClick={() => addNewVideo()}
              >
                Valider la création
              </Button>
            )}
          </Flex>
        </Flex>
      </Box>
    </Box>
  );
};

export default withAuth(Admin);
