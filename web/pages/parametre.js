import {
  Flex,
  Text,
  Box,
  Heading,
  Textarea,
  IconButton,
  useColorMode,
  Button,
  Select,
  Link,
  Image,
  useToast,
} from "@chakra-ui/react";
import SimpleSidebar from "../components/Menu";
import { MoonIcon, SunIcon } from "@chakra-ui/icons";
import { useStore } from "./index";
import { useState } from "react";
import withAuth from "../components/withAuth";
import { updateProfil } from "@mokhta_s/react-statfive-api";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useRouter } from "next/router";

const Parametre = () => {
  const { colorMode, toggleColorMode } = useColorMode();
  const idUser = useStore((state) => state.userValue);
  const dataUser = useStore((state) => state.data);
  const logOut = useStore((state) => state.deleteEverything);
  const [description, setDescription] = useState(
    dataUser ? dataUser.description : ""
  );
  const [poste, setPoste] = useState(dataUser ? dataUser.post : "");

  const toast = useToast();
  const router = useRouter();

  const updateProfilUser = async () => {
    const result = await updateProfil(idUser, description, poste);
    if (result?.data.error === false) {
      toast({
        title: "Profil",
        description: "Votre profil a bien été modifié",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
    } else {
      toast({
        title: "Profil",
        description: "Il y a eu un problème lors de la modification",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const logout = async () => {
    await AsyncStorage.clear();
    router.push("/");
  };

  return (
    <Box>
      <SimpleSidebar />
      <Box
        pos="relative"
        left={{ sm: "100px", md: "240px" }}
        w={{ md: "calc(100% -  240px)" }}
      >
        <Heading textAlign="center" mb="50px">
          Mes paramètres
        </Heading>
        <Flex flexDir="column">
          <Flex mb="25px" justifyContent="center">
            <Text>Changer de mode : </Text>
            <IconButton
              ml="10px"
              size="sm"
              w="auto !important"
              onClick={toggleColorMode}
              icon={colorMode === "dark" ? <SunIcon /> : <MoonIcon />}
              id="toggleColorMode"
              as="div"
              role="button"
            />
          </Flex>
          <Flex justifyContent="center">
            <Flex flexDir="column" mb="25px">
              <Heading>Modifier mes informations :</Heading>
              <Textarea
                datatestid="profil_textarea"
                placeholder="Ajouter une description"
                value={description && description.length > 0 ? description : ""}
                onChange={(e) => setDescription(e.target.value)}
                mt="25px"
              />
              <Select
                datatestid="profil_select"
                placeholder="Choisissez votre poste"
                value={poste && poste.length > 0 ? poste : ""}
                onChange={(e) => setPoste(e.target.value)}
                mt="25px"
              >
                <option value="Attaquant">Attaquant</option>
                <option value="Défenseur">Défenseur</option>
                <option value="Gardien">Gardien</option>
              </Select>
              <Button
                datatestid="profil_button"
                onClick={() => updateProfilUser()}
                mt="25px"
              >
                Enregistrer mes modifications
              </Button>
            </Flex>
          </Flex>
          <Flex flexDirection="column" ml="40px" alignItems="center">
            <Text as="h1" fontWeight="bold">
              Application pour mobile :
            </Text>
            <Flex alignItems="center">
              <Text>
                Vous pouvez scanner le qr code ci-dessous ou bien vous dirigez
                sur ce{" "}
                <Link
                  isExternal
                  color="blue.500"
                  href="exp://exp.host/@fr4nck/StatFiveV3"
                >
                  lien
                </Link>{" "}
                depuis un mobile{" "}
              </Text>
              <Image
                alt="qr-code"
                ml="10px"
                boxSize="150px"
                src="qr-code.png"
              />
            </Flex>
          </Flex>
          <Flex mt="50px">
            <Link m="auto" href="/">
              <Button onClick={() => logout()} color="white" background="black">
                Se déconnecter
              </Button>
            </Link>
            <Button m="auto" w="25%" colorScheme="red" isDisabled>
              Supprimer mon compte
            </Button>
          </Flex>
        </Flex>
      </Box>
    </Box>
  );
};

export default withAuth(Parametre);
