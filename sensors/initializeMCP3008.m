% initializeMCP3008.m
function mcp3008 = initializeMCP3008(rpi)
    mcp3008 = raspi.internal.mcp3008(rpi, 'CE0');
    disp('MCP3008 initialized on CE0.');
end