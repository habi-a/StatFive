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
  
  export default function Card() {
    return (
      <Center py={6}>
        <Box
          maxW={'270px'}
          w={'full'}
          bg={useColorModeValue('white', 'gray.800')}
          boxShadow={'2xl'}
          rounded={'md'}
          overflow={'hidden'}>
          <Image
            h={'120px'}
            w={'full'}
            src={
              'https://information.tv5monde.com/sites/info.tv5monde.com/files/assets/images/Victoire_Algerie.jpg'
            }
            objectFit={'cover'}
          />
          <Flex justify={'center'} mt={-12}>
            <Avatar
              size={'xl'}
              src={
                'https://auth.etna-alternance.net/api/users/mokhta_s/photo'
              }
              alt={'Author'}
              css={{
                border: '2px solid white',
              }}
            />
          </Flex>
  
          <Box p={6}>
            <Stack spacing={0} align={'center'} mb={5}>
              <Heading fontSize={'2xl'} fontWeight={500} fontFamily={'body'}>
                Sofiane Mokhtari
              </Heading>
              <Text color={'gray.500'}>Poste : Défenseur</Text>
              <Text
          textAlign={'center'}
          color={useColorModeValue('gray.700', 'gray.400')}
          px={3}>
          Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        </Text>
            </Stack>
  
        <Text fontWeight="bold" textAlign="center">sofiane.mokhtari@sm.fr</Text>
            <Button
              w={'full'}
              mt={3}
              bg={useColorModeValue('#151f21', 'gray.900')}
              color={'white'}
              rounded={'md'}
              _hover={{
                transform: 'translateY(-2px)',
                boxShadow: 'lg',
              }}>
              Modifier mon profil
            </Button>
          </Box>
        </Box>
      </Center>
    );
  }