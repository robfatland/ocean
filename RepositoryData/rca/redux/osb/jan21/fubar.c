main(p,c){for(p=0;c=~getchar();printf("  %02x"+(p++%16!=8),~c))p%16||printf("\n%08x:"+!p,p);puts("");}
