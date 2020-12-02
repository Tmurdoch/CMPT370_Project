#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

#define FILE_VER_ZERO_HEADER_SIZE 39

struct fileheadstruct
{
	uint8_t magic[20];
	uint8_t version;
	uint8_t gameMode;
	uint8_t aiInGame;
	uint8_t darkPlayerisAI;
	uint8_t darkPlayerTurn;
	uint8_t boardHeight;
	uint8_t boardWidth;
	uint8_t colours;
	uint8_t timerEnabled;
	uint8_t boardColour;
	uint8_t unusedReserved;
	union
	{
		uint32_t lightPlayerTimeb;
		float lightPlayerTime;
	};
	union
	{
		uint32_t darkPlayerTimeb;
		float darkPlayerTime;
	};
}__attribute__((packed));

char *gameType[] = {"Chess", "Checkers"};
char *pcolours[] = {"BROWN_GREY", "PINK_BLUE"};
char *bcolours[] = {"WHITE_BLACK", "RED_GREEN", "YELLOW_BLUE"};


void makeEndianBackwardsForX86CPUS(uint32_t *x)
{
	*x = ((((*x) & 0xff000000u) >> 24) | (((*x) & 0x00ff0000u) >> 8)     \
		| (((*x) & 0x0000ff00u) << 8) | (((*x) & 0x000000ffu) << 24));
	return;
}

int main(int argc, char *argv[])
{
	FILE *fp=NULL;
	long int fps;
	unsigned char *file=NULL;
	unsigned char x, y;
	struct fileheadstruct * filehead;
	//rows columns
	uint8_t *gameboard;
	uint8_t magic[]={'c','m','p','t','3','7','0','c','h','e','c','k','e','r','s','c','h','e','s','s'};
	unsigned char retcode = 0;

	#ifdef __ORDER_LITTLE_ENDIAN__
	printf("LE machine\n");
	#else
	printf("BE machine\n");
	#endif

	if (argc != 2)
	{
		printf("specify file\n");
		return 1;
	}

	fp = fopen(argv[1],"rb");

	if (fp==NULL)
	{
		printf("can't open file\n");
		return 1;
	}

	fseek(fp,0,SEEK_END);
	fps = ftell(fp);
	fseek(fp,0,SEEK_SET);

	if (fps!=FILE_VER_ZERO_HEADER_SIZE+(8*8))
	{
		printf("size of file is incorrect, expected %i got %li\n", FILE_VER_ZERO_HEADER_SIZE+(8*8), fps);
		if (fps==20)
		{
			printf("it is likely the save system crashed while generating the file is exactly as long as the magic\n");
		}
		return 1;
	}

	file = malloc(FILE_VER_ZERO_HEADER_SIZE+(8*8));

	if (file==NULL)
	{
		printf("Download more ram m8\n");
	}

	if (!fread(file, FILE_VER_ZERO_HEADER_SIZE+(8*8), 1, fp))
	{
		printf("couldn't read the whole file for some reason\n");
		return 1;
	}
	fclose(fp);

	filehead = file;

	if (memcmp(magic, file, 20))
	{
		printf("Magic:  \tBAD\n");
	}
	else
	{
		printf("Magic:  \tOK ;-)\n");
	}

	printf("Version:\t%i\n",filehead->version);
	printf("GameMode:\t%i",filehead->gameMode);
	if (filehead->gameMode>=2)
	{
		printf("\tinvalid\n");
		retcode = 1;
	}
	else
	{
		printf("\t%s\n",gameType[filehead->gameMode]);
	}
	printf("aiInGame:\t%i\n",filehead->aiInGame);
	printf("darkisai:\t%i\n",filehead->darkPlayerisAI);
	printf("darkPlayerTurn:\t%i\n",filehead->darkPlayerTurn);
	printf("height: \t%i\n",filehead->boardHeight);
	printf("width:  \t%i\n",filehead->boardWidth);
	printf("Version:\t%i\n",filehead->version);
	printf("pcolour:\t%i",filehead->colours);
	if (filehead->colours >= (sizeof(pcolours)/sizeof(pcolours[0])))
	{
		printf("\tinvalid\n");
		retcode = 1;
	}
	else
	{
		printf("\t%s\n",pcolours[filehead->colours]);
	}
	printf("timer:  \t%i\n",filehead->timerEnabled);
	printf("bcolour:\t%i",filehead->boardColour);
	if (filehead->boardColour >= (sizeof(bcolours)/sizeof(bcolours[0])))
	{
		printf("\tinvalid\n");
		retcode = 1;
	}
	else
	{
		printf("\t%s\n",bcolours[filehead->boardColour]);
	}
	printf("unused: \t%i\n",filehead->unusedReserved);
	#ifdef __ORDER_LITTLE_ENDIAN__
	makeEndianBackwardsForX86CPUS(&(filehead->lightPlayerTimeb));
	makeEndianBackwardsForX86CPUS(&(filehead->darkPlayerTimeb));
	#endif
	printf("ltime:  \t%f\n",filehead->lightPlayerTime);
	printf("dtime:  \t%f\n",filehead->darkPlayerTime);
	gameboard = &file[FILE_VER_ZERO_HEADER_SIZE];
	y=0;
	while (y!=8)
	{
		x=0;
		while (x!=8)
		{
			printf("|%hu|",gameboard[y*8+x]);
			x++;
		}
		printf("\n");
		y++;
	}
	free(file);
	return retcode;
}
