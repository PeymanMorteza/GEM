methods=(pretrained) #PEYMAN
data_models=(cifar10_wrn cifar100_wrn)
gpu=0

if [ "$1" = "MSP" ]; then
    for dm in ${data_models[$2]}; do
        for method in ${methods[0]}; do
            # MSP with in-distribution samples as pos
            echo "-----------"${dm}_${method}" MSP score-----------------"
            CUDA_VISIBLE_DEVICES=$gpu python3 test.py --method_name ${dm}_${method} --num_to_avg 10
        done
    done
    echo "||||||||done with "${dm}_${method}" above |||||||||||||||||||"
elif [ "$1" = "energy" ]; then
    for dm in ${data_models[$2]}; do
        for method in ${methods[0]}; do
            echo "-----------"${dm}_${method}" energy score-----------------"
            CUDA_VISIBLE_DEVICES=$gpu python3 test.py --method_name ${dm}_${method} --num_to_avg 10 --score energy
        done
    done
    echo "||||||||done with "${dm}_${method}" energy score above |||||||||||||||||||"
elif [ "$1" = "M" ]; then
    for dm in ${data_models[$2]}; do
        for method in ${methods[0]}; do
            for noise in 0.0; do
                echo "-----------"${dm}_${method}_M_noise_${noise}"-----------------"
                CUDA_VISIBLE_DEVICES=$gpu python3 test.py --method_name ${dm}_${method} --num_to_avg 10 --score M --noise $noise -v
            done
        done
    done
    echo "||||||||done with "${dm}_${method}_M" noise above|||||||||||||||||||"
elif [ "$1" = "GEM" ]; then
    for dm in ${data_models[$2]}; do
        for method in ${methods[0]}; do
            for noise in 0.0; do
                echo "-----------"${dm}_${method}_M_noise_${noise}"-----------------"
                CUDA_VISIBLE_DEVICES=$gpu python3 test.py --method_name ${dm}_${method} --num_to_avg 10 --score GEM --noise $noise -v
            done
        done
    done
    echo "||||||||done with "${dm}_${method}_GEM" noise above|||||||||||||||||||"
elif [ "$1" = "Odin" ]; then
    for T in 1000 100 10 1; do
	for noise in 0; do
            echo "-------T="${T}_$2"   noise="$noise"--------"
	    CUDA_VISIBLE_DEVICES=$gpu python3 test.py --method_name $2  --score Odin --num_to_avg 10 --T $T --noise $noise -v #--test_bs 50
	done
        echo "||||Odin temperature|||||||||||||||||||||||||||||||||||||||||||"
    done
elif [ "$1" = "T" ]; then
    for dm in ${data_models[@]}; do
        for method in ${methods[0]}; do
            for T in 1 2 5 10 20 50 100 200 500 1000; do
                echo "-----------"${dm}_${method}_T_${T}"-----------------"
                CUDA_VISIBLE_DEVICES=$gpu python3 test.py --method_name ${dm}_${method} --num_to_avg 10 --score energy --T $T
            done
        done
        echo "||||||||done with "${dm}_${method}_T" tempearture above|||||||||||||||||||"
    done
fi

