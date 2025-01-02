#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cmath>

using namespace std;

const int SLOT_TIME = 51;
const int MAX_FRAME_LENGTH = 5;
const int MAX_BACKOFF_EXP = 10; 

void simulateCSMACD(int N, int total_slots) {
    vector<int> transmission_start_time(N, -1); 
    vector<int> backoff_time(N, 0); 
    vector<bool> has_transmitted(N, false); 
    vector<int> collision_count(N, 0); 

    int current_time = 0; 

    while (current_time < total_slots) {
        int active_stations = 0; 
        vector<int> stations_transmitting; 
        cout << "\nCurrent time slot: " << current_time << endl;
        cout << "Backoff times: ";
        for (int i = 0; i < N; i++) {
            cout << "Station " << i + 1 << ": " << backoff_time[i] << " | ";
        }
        cout << endl;
        for (int i = 0; i < N; i++) {
            if (backoff_time[i] > 0) {
                backoff_time[i]--; 
            }
        }
        for (int i = 0; i < N; i++) {
            if (!has_transmitted[i]) {
                if (backoff_time[i] == 0) { 
                    active_stations++;
                    stations_transmitting.push_back(i);
                    cout << "Station " << i + 1 << " attempts to transmit." << endl;
                }
            }
        }

        if (active_stations == 1) {
            int station = stations_transmitting[0];
            transmission_start_time[station] = current_time;
            has_transmitted[station] = true;

            cout << "Station " << station + 1 << " successfully starts transmitting at time slot " << current_time << endl;
            int frame_duration = MAX_FRAME_LENGTH;
            current_time += frame_duration;

            for (int i = 0; i < N; i++) {
                if (!has_transmitted[i] && backoff_time[i] > 0) {
                    backoff_time[i] = max(0, backoff_time[i] - frame_duration); // Reduce backoff by frame duration
                }
            }
        } else if (active_stations > 1) {
            // If more than one station transmits, a collision occurs
            cout << "Collision detected at time slot " << current_time << " among stations: ";
            for (int station : stations_transmitting) {
                cout << station + 1 << " ";
                
                // Increase the collision count and apply exponential backoff
                collision_count[station]++;
                int backoff_exponent = min(collision_count[station], MAX_BACKOFF_EXP);
                int max_backoff_slots = pow(2, backoff_exponent) - 1;
                
                backoff_time[station] = rand() % max_backoff_slots + 1;
                cout << "(new backoff: " << backoff_time[station] << ") ";
            }
            cout << endl;
            current_time += 1; 
        } else {
            current_time++;
        }

        bool all_transmitted = true;
        for (int i = 0; i < N; i++) {
            if (!has_transmitted[i]) {
                all_transmitted = false;
                break;
            }
        }
        if (all_transmitted) {
            break;
        }
    }
    for (int i = 0; i < N; i++) {
        if (!has_transmitted[i]) {
            cout << "Station " << i + 1 << " did not successfully transmit within the simulation time." << endl;
        }
    }
}

int main() {
    srand(time(0)); 

    int N, total_slots;
    cout << "Enter the number of stations: ";
    cin >> N;
    cout << "Enter the total number of time slots to simulate: ";
    cin >> total_slots;

    simulateCSMACD(N, total_slots);

    return 0;
}