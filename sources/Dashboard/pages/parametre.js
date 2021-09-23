import { Flex, Text, Box, Heading, List, ListItem, ListIcon, Link, IconButton, useColorMode, Button } from '@chakra-ui/react'
import SimpleSidebar from "../components/Menu"
import { MoonIcon, SunIcon } from "@chakra-ui/icons";

export default function Parametre() {
    const { colorMode, toggleColorMode } = useColorMode();

  return (
    <Box>
        <SimpleSidebar />
        <Box pos="relative" left="240px" w="calc(100% -  240px)">
            <Heading textAlign="center" mb="50px">Mes paramètres</Heading>
            <Flex flexDir="column" >
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
                <Button m="auto" w="25%" bgColor="red.400" color="red.50">Supprimer mon compte</Button>
            </Flex>
        </Box>
    </Box>
  )
}
