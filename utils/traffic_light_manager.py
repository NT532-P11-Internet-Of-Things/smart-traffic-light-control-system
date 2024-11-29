import time


class TrafficLightManager:
    def __init__(self, num_lanes=4):
        self.lanes = [
            {
                'id': lane_id,
                'is_green': lane_id in [2, 4],  # True/False: Mặc định làn 2 và 4 có đèn xanh
                'green_time': 10,  # Thời gian đèn xanh mặc định
                'red_time': 13,  # Thời gian đèn đỏ mặc định
                'remaining_time': 10,  # Thời gian còn lại của đèn
                'start_time': time.time(),  # Thời điểm bắt đầu lượt
                'vehicles_at_change': 0,  # Số xe tại thời điểm chuyển đèn
                'total_vehicles': 0,  # Tổng số xe trong làn
                'cycle_count': 0  # Số lần chu kỳ đèn giao thông
            } for lane_id in range(1, num_lanes + 1)
        ]
        self.opposite_pairs = [(1, 3), (2, 4)]

    def update_lane(self, lane_id, vehicles_count):
        """Cập nhật thông tin xe và trạng thái cho một làn"""
        for lane in self.lanes:
            if lane['id'] == lane_id:
                lane['total_vehicles'] = vehicles_count
                break

    def update_vehicle_at_change(self, lane_id, vehicles_at_change):
        """Cập nhật thông tin xe và trạng thái cho một làn"""
        for lane in self.lanes:
            if lane['id'] == lane_id:
                lane['vehicles_at_change'] = vehicles_at_change
                lane['cycle_count'] += 1
                break
    def switch_traffic_lights(self, lane_timers):
        """Chuyển trạng thái đèn giao thông cho các làn đối diện"""
        green_time = self.schedule()

        for pair in self.opposite_pairs:
            lane1, lane2 = pair
            lane1_obj = next(lane for lane in self.lanes if lane['id'] == lane1)
            lane2_obj = next(lane for lane in self.lanes if lane['id'] == lane2)

            # Chuyển trạng thái đèn
            lane1_obj['is_green'] = not lane1_obj['is_green']
            lane2_obj['is_green'] = not lane2_obj['is_green']

            # Cập nhật thời gian và số xe tại thời điểm chuyển
            for lane in [lane1_obj, lane2_obj]:
                lane['green_time'] = green_time
                lane['red_time'] = green_time + 3
                lane['remaining_time'] = lane['green_time'] if lane['is_green'] else lane['red_time']
                lane['start_time'] = time.time()
                lane['vehicles_at_change'] = lane['total_vehicles']
                lane['cycle_count'] += 1

        return self.lanes

    def schedule(self):
        """Synchronize green times for opposite lane pairs"""
        green_time = 0
        max_vehicles = 0

        # Duyệt qua từng cặp làn đối diện
        for pair in self.opposite_pairs:
            # Lấy đối tượng làn dựa trên ID
            lane1_obj = next(lane for lane in self.lanes if lane['id'] == pair[0])
            lane2_obj = next(lane for lane in self.lanes if lane['id'] == pair[1])

            # Kiểm tra xem trạng thái đèn xanh của cả hai làn
            if not lane1_obj['is_green'] and not lane2_obj['is_green']:
                # Tính số lượng xe lớn nhất của cặp làn này
                vehicles = max(lane1_obj['total_vehicles'], lane2_obj['total_vehicles'])
                print("Số lượng xe được tính:", vehicles)

                # Tính thời gian đèn xanh dựa trên số xe
                green_time = min(max(10 + vehicles * 0.5, 5), 30)
                print("Thời gian green_time:", green_time)

        return green_time

    def update_remaining_time(self):
        """Cập nhật thời gian còn lại cho mỗi làn"""
        current_time = time.time()
        for lane in self.lanes:
            elapsed_time = current_time - lane['start_time']

            if lane['is_green']:
                lane['remaining_time'] = max(0, lane['green_time'] - elapsed_time)
                if lane['remaining_time'] <= 0:
                    lane['start_time'] = current_time
                    lane['remaining_time'] = lane['red_time']
            else:
                lane['remaining_time'] = max(0, lane['red_time'] - elapsed_time)
                if lane['remaining_time'] <= 0:
                    lane['start_time'] = current_time
                    lane['remaining_time'] = lane['green_time']

    def get_lane_status(self, lane_id):
        """Lấy trạng thái chi tiết của một làn"""
        for lane in self.lanes:
            if lane['id'] == lane_id:
                return lane
        return None

    def get_all_lanes_status(self):
        """Lấy trạng thái của tất cả các làn"""
        return self.lanes