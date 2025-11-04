def calculate_last_n_stats(last_balls_string, n_balls=24):
    balls = last_balls_string.strip().split()
    runs_last_6 = 0
    wickets_last_6 = 0

    for ball in balls:
        if ball.upper() == 'W':
            wickets_last_6 += 1
        else:
            try:
                runs_last_6 += int(ball)
            except ValueError:
                pass

    scaling_factor = n_balls / len(balls)

    runs_in_last_n_proj = runs_last_6 * scaling_factor
    wickets_in_last_n_proj = wickets_last_6 * scaling_factor

    return runs_in_last_n_proj, wickets_in_last_n_proj