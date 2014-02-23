#include <boost/asio/serial_port.hpp> 
#include <boost/asio.hpp> 
#include <stdlib.h>

#include "XimuReceiver.h"

using namespace boost;


int main(int argc, char** argv) {
	asio::io_service io;
	asio::serial_port port(io);

	port.open("COM16");
	port.set_option(asio::serial_port_base::baud_rate(115200));

	XimuReceiver receiver;

	char c;

	while (true) {
		// Read 1 character into c, this will block
		// forever if no character arrives.
		asio::read(port, asio::buffer(&c,1));
		receiver.processNewChar(c);

		if (receiver.isInertialAndMagGetReady() && receiver.isQuaternionGetReady()) {
			DrumSet drum = receiver.getDrum();
			if (drum.drumID > 0 && drum.strength > 1) {
				std::string command = "python ../frontend/midiPlayer.py ";
				command.append(std::to_string(drum.drumID));
				command.append(" ");
				command.append(std::to_string(drum.strength));
				char* commands;
				std::strcpy(commands,command.c_str());
				// System call to run python codes
				std::system(commands);
			}
		}
	}
	
	return 0;
}