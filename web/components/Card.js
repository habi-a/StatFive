import {
    Heading,
    Avatar,
    Box,
    Center,
    Image,
    Flex,
    Text,
    Stack,
    Button,
    useColorModeValue,
    Link
  } from '@chakra-ui/react';

import {useStore} from "../pages/index"
  
  export default function Card({info, delUser, cantDelete}) {
    const removeSpecificID = useStore(state => state.resetID)
    const test = useStore(state => state.teamUser)

    console.log(info)

    const userDelete = () => {
      delUser(false);
      removeSpecificID(info.id)
    }

    return (
      <Center py={6}>
        <Box
          maxW={'450px'}
          h="225px"
          w={'full'}
          bg={useColorModeValue('white', 'gray.800')}
          boxShadow={'2xl'}
          rounded={'md'}
          overflow={'hidden'}>
  
          <Box p={6}>
            <Stack spacing={0} align={'center'} mb={5}>
              <Heading fontSize={'2xl'} fontWeight={500} fontFamily={'body'}>
                {info.firstname} {info.lastname} 
              </Heading>
              <Text color={'gray.500'}>Poste : {info.post}</Text>
              <Text
          textAlign={'center'}
          color={useColorModeValue('gray.700', 'gray.400')}
          px={3}>
          {info.description}
        </Text>
        {cantDelete === undefined && <Button onClick={() => userDelete()} size="xs" mt="25px !important" colorScheme="red">Supprimer le joueur </Button> }
            </Stack>
          </Box>
        </Box>
      </Center>
    );
  }